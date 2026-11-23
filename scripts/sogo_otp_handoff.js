// Paste this helper into the Codex cua_repl JavaScript context.
// It opens MyMeet authorization messages in the visible SOGo order (check that
// the message list is date-descending) until the newest one for the requested
// alias is found. The validated
// code goes on the browser clipboard for 60 seconds, then the prior value is
// restored only if the clipboard still contains this code. It never prints or
// enters the code, and never submits a form.

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

async function handoffNewestMyMeetCode(tab, expectedRecipient) {
  const initial = await tab.getAXState({ emit: false, disableDiffing: true });
  if (!initial.includes("messagesList")) {
    throw new Error("SOGo message list is not open");
  }
  const candidates = tab.playwright.getByRole("button", {
    name: "Your authorisation code",
    exact: true,
  });
  const count = await candidates.count();
  let parsed;
  for (let index = 0; index < count; index += 1) {
    await candidates.nth(index).click();
    await tab.playwright.getByText("To", { exact: true }).last().waitFor({
      state: "visible",
      timeout: 5_000,
    });
    const snapshot = await tab.getAXState({ emit: false, disableDiffing: true });
    try {
      parsed = parseSelectedMyMeetCode(snapshot, expectedRecipient);
      break;
    } catch (error) {
      const reason = error instanceof Error ? error.message : "message_unreadable";
      if (reason === "selected message recipient does not match the requested alias") continue;
      if (reason === "authorization email is outside the 10-minute freshness window") break;
      throw error;
    }
  }
  if (!parsed) throw new Error("no fresh MyMeet authorization email for the requested alias");

  const previousClipboard = await tab.clipboard.readText();
  await tab.clipboard.writeText(parsed.code);
  setTimeout(async () => {
    try {
      if ((await tab.clipboard.readText()) === parsed.code) {
        await tab.clipboard.writeText(previousClipboard);
      }
    } catch {
      // Never replace newer clipboard contents or surface secret data in errors.
    }
  }, 60_000);
  return { copied: true, recipient: parsed.recipient, sentAt: parsed.sentAt, expiresInSeconds: 60 };
}

// Example in the CUA context after defining the functions above:
// const mailTabs = await cua.listTabs({ browser: "iab" });
// const mailTabInfo = mailTabs.find((item) => item.url?.startsWith("https://mail.iqdoctor.pro/SOGo/"));
// if (!mailTabInfo) throw new Error("SOGo tab not found");
// const mailTab = await cua.getTab(mailTabInfo.id, { browser: "iab" });
// const result = await handoffNewestMyMeetCode(mailTab, "alias@iqdoctor.pro");
// nodeRepl.write(JSON.stringify(result));
