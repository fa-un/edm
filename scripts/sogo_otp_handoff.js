// Paste this helper into the Codex cua_repl JavaScript context. It reads a
// fresh MyMeet authorization email from SOGo, fills the code into the matching
// MyMeet verification screen, and presses Confirm. It never prints or returns
// the code. The separate initializer below sets a random password only during
// first-time account creation; it does not handle password changes or resets.

function randomPassword(length = 28) {
  if (!globalThis.crypto?.getRandomValues) {
    throw new Error("secure random generator is unavailable in this runtime");
  }
  if (!Number.isInteger(length) || length < 20 || length > 128) {
    throw new Error("initial password length must be between 20 and 128");
  }

  const groups = [
    "abcdefghijkmnopqrstuvwxyz",
    "ABCDEFGHJKLMNPQRSTUVWXYZ",
    "23456789",
    "!@#$%^&*()-_=+",
  ];
  const alphabet = groups.join("");
  const randomBelow = (bound) => {
    const limit = Math.floor(256 / bound) * bound;
    let value;
    do {
      const byte = new Uint8Array(1);
      globalThis.crypto.getRandomValues(byte);
      value = byte[0];
    } while (value >= limit);
    return value % bound;
  };
  const pick = (chars) => chars[randomBelow(chars.length)];

  const chars = groups.map(pick);
  while (chars.length < length) chars.push(pick(alphabet));
  for (let index = chars.length - 1; index > 0; index -= 1) {
    const swapIndex = randomBelow(index + 1);
    [chars[index], chars[swapIndex]] = [chars[swapIndex], chars[index]];
  }
  return chars.join("");
}

async function initializeMyMeetPassword(myMeetTab) {
  const pageUrl = new URL(await myMeetTab.playwright.evaluate("() => location.href"));
  if (pageUrl.origin !== "https://app.mymeet.ai" || !/^\/sign-up(?:\/|$)/i.test(pageUrl.pathname)) {
    throw new Error("initial password setup is allowed only in the MyMeet sign-up flow");
  }

  let state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
  if (/We sent verification code on your email/i.test(state)) {
    throw new Error("confirm the email code before initializing the account password");
  }
  const passwordFieldIndexes = state.split(/\r?\n/)
    .filter((line) => /\b(?:secure )?text field\b|\bpassword field\b/i.test(line) && /password/i.test(line) && /settable/i.test(line))
    .map((line) => Number(line.match(/^\s*(\d+)/)?.[1]))
    .filter(Number.isFinite);
  if (passwordFieldIndexes.length !== 2) {
    throw new Error("expected exactly two accessible password fields on the initial setup form");
  }

  const submitIndexes = [...state.matchAll(/^\s*(\d+) button (?:Create account|Create my account|Set password|Continue)$/gim)]
    .map((match) => Number(match[1]));
  if (submitIndexes.length !== 1) {
    throw new Error("expected exactly one account-creation or initial-password submit button");
  }

  let password = randomPassword();
  try {
    await myMeetTab.setValue(passwordFieldIndexes[0], password);
    await myMeetTab.setValue(passwordFieldIndexes[1], password);
    state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
    const currentSubmitIndexes = [...state.matchAll(/^\s*(\d+) button (?:Create account|Create my account|Set password|Continue)$/gim)]
      .map((match) => Number(match[1]));
    if (currentSubmitIndexes.length !== 1) {
      throw new Error("initial password form changed before submission");
    }
    const currentUrl = new URL(await myMeetTab.playwright.evaluate("() => location.href"));
    if (currentUrl.origin !== "https://app.mymeet.ai" || !/^\/sign-up(?:\/|$)/i.test(currentUrl.pathname)) {
      throw new Error("MyMeet left the account-creation flow before password submission");
    }
    await myMeetTab.click(currentSubmitIndexes[0]);
    state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
    const finalUrl = await myMeetTab.playwright.evaluate("() => location.href");
    return {
      submitted: true,
      accountSetupAdvanced: !/^\/sign-up(?:\/|$)/i.test(new URL(finalUrl).pathname),
      finalUrl,
      passwordPersistedLocally: false,
    };
  } finally {
    password = "";
  }
}

function parseSelectedMyMeetCode(snapshot, expectedRecipient, now = new Date()) {
  const emailPattern = /[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}/gi;
  const toIndex = snapshot.lastIndexOf("text To");
  if (toIndex < 0) throw new Error("selected message has no recipient header");

  const header = snapshot.slice(Math.max(0, toIndex - 1200), toIndex);
  const message = snapshot.slice(toIndex);
  if (!/hello@mymeet\.ai/i.test(header)) throw new Error("selected message is not from MyMeet");
  if (!/Your authorisation code/i.test(header)) throw new Error("selected message is not an authorization-code email");

  // SOGo renders recipient chips immediately below the To label. Restrict
  // matching to those first rows so footer links cannot look like recipients.
  const recipientBlock = message.split(/\r?\n/).slice(0, 4).join("\n");
  const recipients = [...new Set(recipientBlock.match(emailPattern) ?? [])];
  if (recipients.length !== 1 || recipients[0].toLowerCase() !== expectedRecipient.toLowerCase()) {
    throw new Error("selected message recipient does not match the requested alias");
  }

  const sentMatch = header.match(/text\s+([A-Z][a-z]+,\s+[A-Z][a-z]+\s+\d{1,2},\s+\d{4}\s+\d{1,2}:\d{2}\s+[+-]\d{2}(?::?\d{2})?)/);
  if (!sentMatch) throw new Error("selected message timestamp could not be read");
  const timestampText = sentMatch[1].replace(/([+-]\d{2})$/, "$1:00");
  const sentAt = new Date(timestampText);
  if (Number.isNaN(sentAt.getTime())) throw new Error("selected message timestamp is invalid");
  const ageMs = now.getTime() - sentAt.getTime();
  if (ageMs < -2 * 60_000 || ageMs > 10 * 60_000) throw new Error("authorization email is outside the 10-minute freshness window");

  const codeMatch = message.match(/button\s+mymeet\.ai\s+Your authorisation code\s+(\d{6})\b/i);
  if (!codeMatch) throw new Error("six-digit code not found in selected message body");
  return { code: codeMatch[1], recipient: recipients[0], sentAt: sentAt.toISOString() };
}

async function newestMyMeetCode(tab, expectedRecipient) {
  const pageUrl = new URL(await tab.playwright.evaluate("() => location.href"));
  if (pageUrl.origin !== "https://mail.iqdoctor.pro" || !pageUrl.pathname.includes("/SOGo/")) {
    throw new Error("SOGo tab must be open at mail.iqdoctor.pro/SOGo");
  }

  const initial = await tab.getAXState({ emit: false, disableDiffing: true });
  if (!initial.includes("messagesList")) {
    throw new Error("SOGo message list is not open");
  }
  const candidates = tab.playwright.getByRole("button", {
    name: "Your authorisation code",
    exact: true,
  });
  const count = await candidates.count();
  let newest;
  for (let index = 0; index < count; index += 1) {
    await candidates.nth(index).click();
    await tab.playwright.getByText("To", { exact: true }).last().waitFor({
      state: "visible",
      timeout: 5_000,
    });
    const snapshot = await tab.getAXState({ emit: false, disableDiffing: true });
    try {
      const parsed = parseSelectedMyMeetCode(snapshot, expectedRecipient);
      if (!newest || Date.parse(parsed.sentAt) > Date.parse(newest.sentAt)) {
        newest = parsed;
      }
    } catch (error) {
      const reason = error instanceof Error ? error.message : "message_unreadable";
      if (reason === "selected message recipient does not match the requested alias") continue;
      if (reason === "authorization email is outside the 10-minute freshness window") continue;
      throw error;
    }
  }
  if (!newest) throw new Error("no fresh MyMeet authorization email for the requested alias");
  return newest;
}

async function confirmNewestMyMeetCode(mailTab, myMeetTab, expectedRecipient) {
  if (!/^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$/i.test(expectedRecipient)) {
    throw new Error("a valid expected alias is required");
  }

  const myMeetUrl = new URL(await myMeetTab.playwright.evaluate("() => location.href"));
  if (myMeetUrl.origin !== "https://app.mymeet.ai" || !/\/(sign-up|sign-in)\/?$/i.test(myMeetUrl.pathname)) {
    throw new Error("MyMeet must be on its sign-up or sign-in verification screen");
  }

  let state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
  if (!state.includes("We sent verification code on your email")) {
    throw new Error("MyMeet is not waiting for an email verification code");
  }

  const parsed = await newestMyMeetCode(mailTab, expectedRecipient);
  const fieldIndexes = [...state.matchAll(/^\s*(\d+) text field \(settable\)/gm)]
    .map((match) => Number(match[1]));
  if (fieldIndexes.length !== 1) {
    throw new Error("verification screen must contain exactly one editable text field");
  }

  await myMeetTab.setValue(fieldIndexes[0], parsed.code);
  state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
  const currentUrl = new URL(await myMeetTab.playwright.evaluate("() => location.href"));
  if (currentUrl.origin !== "https://app.mymeet.ai") {
    throw new Error("MyMeet navigated away before verification could be confirmed");
  }

  if (state.includes("We sent verification code on your email")) {
    const confirmIndexes = [...state.matchAll(/^\s*(\d+) button Confirm$/gm)]
      .map((match) => Number(match[1]));
    if (confirmIndexes.length !== 1) {
      throw new Error("verification screen must contain exactly one Confirm button");
    }
    await myMeetTab.click(confirmIndexes[0]);
    state = await myMeetTab.getAXState({ emit: false, disableDiffing: true });
  }

  const finalUrl = await myMeetTab.playwright.evaluate("() => location.href");
  return {
    recipient: parsed.recipient,
    sentAt: parsed.sentAt,
    submitted: true,
    verificationAdvanced: !state.includes("We sent verification code on your email"),
    finalUrl,
  };
}

// Example in the CUA context after defining the functions above:
// const tabs = await cua.listTabs({ browser: "iab" });
// const mailInfo = tabs.find((tab) => tab.url?.startsWith("https://mail.iqdoctor.pro/SOGo/"));
// const myMeetInfo = tabs.find((tab) => tab.url?.startsWith("https://app.mymeet.ai/"));
// if (!mailInfo || !myMeetInfo) throw new Error("SOGo or MyMeet tab not found");
// const mailTab = await cua.getTab(mailInfo.id, { browser: "iab" });
// const myMeetTab = await cua.getTab(myMeetInfo.id, { browser: "iab" });
// const result = await confirmNewestMyMeetCode(mailTab, myMeetTab, "alias@iqdoctor.pro");
// nodeRepl.write(JSON.stringify(result));
// After email verification, when MyMeet displays the first-time setup form:
// const result = await initializeMyMeetPassword(myMeetTab);
// nodeRepl.write(JSON.stringify(result));
