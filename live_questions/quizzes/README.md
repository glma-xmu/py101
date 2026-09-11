# In-class quizzes

Teacher controls are on `/teacher/`, beneath **Your classroom**. Students enter
only at `/quiz/`. No entrance is added to the course navigation or search.

## Run a quiz session

1. Sign in at `/teacher/` with the live-question teacher password.
2. Under **Your classroom**, select **Start quiz**. This is also available after
   **End class** returns the live-question panel to its initial state.
3. Share `/quiz/` and the displayed temporary code. One code opens the entire
   library of current and past quizzes for two hours.
4. Select **End quiz** to revoke access. Students check every five seconds while
   visible and when returning to the tab. Saved copies cannot be recalled.

The code is per access session, not per quiz. No individual publishing step is
needed. Keep old JSON files to preserve past quizzes; add a new file before each
class. All files in this directory are available to students during an active
session; keep unfinished drafts elsewhere. New files and edits appear on refresh.
No answers, grading, or student submissions are included.

Live-question classrooms and quiz sessions operate independently. **End class**
ends only live questions; **End quiz** ends only quiz access. Teacher sign-out,
service restart, or the two-hour quiz timeout revokes quiz access. Access state
is kept only in memory, while quiz files persist on disk.

## Edit before class

Edit `0912.json` or `0919.json` in this directory. Each file has a `title`, an
optional `description`, and a nonempty `questions` array. Each question contains:

- `prompt`: question text, required.
- `code`: optional code to display, with `\n` for line breaks.
- `after`: optional text displayed after the code, with `\n` for line breaks.
- `options`: optional list of choices.

Display order is `prompt`, `code`, `after`, then `options`. No answer fields are needed.

```json
{
  "prompt": "Consider the following Python list:",
  "code": "values = [12, 15, 18, 30, 21, 16]",
  "after": "Write one expression for each task:\n\n1. Extract the third element.\n2. Extract the second-to-last element."
}
```

Text is displayed literally: HTML is not executed and Markdown is not parsed.
For a new class, copy a file to a name such as `0926.json` and edit its contents.
Use lowercase letters, digits, and hyphens in filenames. It appears automatically
in `/quiz/`, with its own link `/quiz/0926/`. Files are read on each request;
refresh the page after saving. No service restart is needed for content edits.
Do not place quiz JSON files in `docs/` or the public static assets folder.

## Deploy

The static MkDocs deployment alone does not install this feature. Update the
existing `live_questions` service (including this directory and the new static
assets), retain its existing password configuration, and restart it for the new
routes. Add the `/quiz` and `/quiz/` locations from
`../deploy/nginx-locations.conf` to the existing HTTPS server configuration,
validate with `sudo nginx -t`, and reload Nginx. Later content-only updates need
only the edited JSON files copied into the service's `quizzes/` directory.

Locally, use the same Uvicorn setup documented in `../README.md`. A plain static
`http.server` serving `site/` cannot handle authentication or `/quiz/`.
