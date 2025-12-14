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

Notes & next steps:
- Next: implement NextAuth API route at app/api/auth/[...nextauth]/route.ts using `lib/auth.ts` options and (optionally) the MongoDB adapter.
- Implement signup API route to create users (hash password + create `users` collection entry and corresponding `UserExtension`).
- Create API routes for posts, post/[id] (like, comment), follow/unfollow, and user/[username].
- Build frontend pages: signup, login, home feed, create post, profile, post detail using existing app/ and components/ structure.
- Add optimistic UI updates (likes, follows) and use sonner to show toasts.

If you want, I'll implement the NextAuth API route and signup API next (recommended).