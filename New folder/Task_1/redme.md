Progress Summary — Mini Instagram Clone


Completed (so far):
- Implemented Mongoose connection singleton: lib/mongooseConnect.ts
- Added Mongoose models:
  - models/UserExtension.ts (username, bio, profilePic, followers, following)
  - models/Post.ts (author, imageUrl, caption, likes, comments)
- Added Zod validation schemas:
  - schemas/authSchema.ts (signup/login)
  - schemas/postSchema.ts (create post)
- Added basic NextAuth helpers and a minimal Credentials-based options object:
  - lib/auth.ts (password hash/verify + credentials authorize implementation using the `users` collection)
- Implemented NextAuth route: app/api/auth/[...nextauth]/route.ts
- Signup API: app/api/auth/signup/route.ts (validates signup, creates `users` entry and `UserExtension`)
- Posts API: app/api/posts/route.ts (GET feed for following + self, POST create)
- Post routes: app/api/post/[id]/route.ts (GET single post), app/api/post/[id]/like/route.ts (toggle like), app/api/post/[id]/comment/route.ts (add comment)
- Follow API: app/api/follow/route.ts (toggle follow/unfollow updates both users atomically)
- Frontend pages & components:
  - `app/(auth)/signup/page.tsx` and `app/(auth)/login/page.tsx` (forms using react-hook-form + zod)
  - `app/page.tsx` — Home feed client that fetches `/api/posts`
  - `components/Postcard.tsx` — post UI with optimistic like and comments UI
  - `app/create/page.tsx` — create post form
  - `app/profile/[username]/page.tsx` — profile page fetching `/api/user/[username]` with follow toggle and post list

Notes & next steps:
- Remaining: polish styling, add server-side rendering for pages where desired, wire NextAuth adapter if you want DB-backed sessions, implement post detail page (`app/post/[id]/page.tsx`) UI enhancements, and add tests.
- I used the env variables from your `.env.local` (for `MONGODB_URI`, `NEXTAUTH_URL`, `NEXTAUTH_SECRET`) when the app runs; ensure they are present.

If you want, next I can:


If you want, next I can:
- Add more polish: typography scale, color accents, and responsive tweaks.
- Add small UI animations and hover states across the app.

Recent UI improvements applied:
- Added `NavBar` with avatar and username (fetches `/api/me`).
- Improved `Postcard` with `Avatar`, image loading skeleton, hover shadow and subtle transform.
- Added loading skeletons for home feed and post detail.
- Made profile posts grid responsive (`sm:2cols`, `lg:3cols`).

Next suggestions:
- Fine-tune color variables in `globals.css` for brand accent.
- Add image optimization or lazy-loading for large images.
- Add unit/e2e tests for core APIs and UI flows.
