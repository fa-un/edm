# MyMeet bridge

`mymeet_bridge.py` receives one raw transcript from the Codex in-app browser
and writes a new UTF-8 Markdown file locally. It does not download recordings,
call MyMeet, change an account, or save a password.

## Save a transcript

1. In the MyMeet meeting, select **Default Meeting** if processing options are
   shown, open **Transcript**, and click **Copy**. Confirm the copied text
   begins and ends with the transcript currently visible in that meeting.
2. In a terminal at the repository root, start a receiver using a new output
   path that does not already exist:

   ```sh
   python3 scripts/mymeet_bridge.py receive \
     --output /Users/vp/edm/Транскрибации/аудиозаписей/YYYY-MM-DD_HH-MM-SS_MyMeet.md
   ```

   The process prints a short-lived localhost URL and waits up to 120 seconds.
   Do not share that URL; it contains a one-use token. The receiver accepts at
   most 25 MiB and binds only to `127.0.0.1`.
3. In the Codex `cua_repl` JavaScript context, locate the MyMeet tab and send its
   tab clipboard directly to that URL. Replace the URL below with the one
   printed by the receiver. Do not print or paste the transcript itself into a
   shell command.

   ```js
   const tabs = await cua.listTabs({ browser: "iab" });
   const meeting = tabs.find((item) => item.url?.startsWith("https://app.mymeet.ai/"));
   if (!meeting) throw new Error("MyMeet tab not found");
   const tab = await cua.getTab(meeting.id, { browser: "iab" });
   const transcript = await tab.clipboard.readText();
   if (!transcript.trim()) throw new Error("Transcript clipboard is empty");
   const response = await fetch("http://127.0.0.1:PORT/receive/ONE_TIME_TOKEN", {
     method: "POST",
     headers: { "Content-Type": "text/plain; charset=utf-8" },
     body: transcript,
   });
   const receipt = await response.json();
   if (!response.ok || !receipt.ok) throw new Error(receipt.error ?? "Save failed");
   nodeRepl.write(JSON.stringify(receipt));
   ```

4. Verify the returned path, byte count, and SHA-256. The receiver confirms a
   byte-for-byte UTF-8 round trip and creates the destination atomically; it
   refuses an existing destination, empty payload, malformed UTF-8, bad token,
   and oversized request. Then compare the saved file's first/last transcript
   lines and timestamps with MyMeet and record any coverage gap.

The bridge prints only its one-time URL and the final metadata receipt. It does
not log request lines or transcript content. A timeout leaves no transcript
file; rerun the command to obtain a fresh token.

## Passwords and email codes

Create temporary email aliases in mailcow at <https://mail.iqdoctor.pro>
(usually admin@iqdoctor.pro → **Temporary email aliases**). Read verification
messages separately in SOGo at <https://mail.iqdoctor.pro/SOGo> (Inbox/Junk).
They are different services with separate login forms, sessions, and menus;
being signed into one does not mean the other is signed in. Check both URL and
page title before acting. Create aliases only in mailcow and retrieve mail only
in SOGo. After checking MyMeet messages, move all MyMeet mail from Inbox to the
`Inbox/mymeet` subfolder. Leave other mail untouched and verify both folders.

After email verification, the helper can initialize the password only on
MyMeet's first-time sign-up form. `initializeMyMeetPassword(myMeetTab)` requires
exactly two accessible password fields and one account-creation/initialization
button. It generates a random 28-character password in memory, fills both
fields, and submits that initial setup form. It returns no password and does
not save or print it. Use this only for the new temporary account; do not plan
another login after transcription. It does not handle a password change or
reset.

If the helper cannot recognize the form, generate a temporary password for
manual entry with:

```sh
python3 scripts/password_handoff.py
```

The small local window shows a random 24-character value, supports regeneration,
and closes after five minutes. It does not print or save the password, place it
on the clipboard, or fill/submit the browser form. The user enters and confirms
the password and submits the form. Close the window when done. Do not put the
value in shell arguments, files, or logs.

Email-code entry is in `scripts/sogo_otp_handoff.js`. Paste the helper into the
Codex `cua_repl` context and call the example at its end with the exact alias
being registered. It checks that the tabs are SOGo and MyMeet, finds the
freshest code for that alias from the visible SOGo messages, requires a MyMeet
sender and a message no older than ten minutes, fills the MyMeet verification
field, and clicks **Confirm**. It never prints or returns the code. Its result
contains only the recipient, email time, final URL, and whether verification
advanced. After verification, call `initializeMyMeetPassword(myMeetTab)` to set
the random password during first-time account creation. Do not use that helper
for password changes/resets, and do not store verification codes or passwords.
