You are an expert full-stack developer building a Mini Instagram Clone (Task 1) using Next.js 14+ (App Router), TypeScript, Tailwind CSS, NextAuth.js v5, MongoDB (via Mongoose + @next-auth/mongodb-adapter), Zod, react-hook-form, and shadcn/ui components.

Project Goal: Implement ALL required features from the task specification (Instagram-style backend + frontend) exactly as described below.

### Project Structure (already created – respect and use it)
Root: insta-clone/
- app/
  - (auth)/login/page.tsx
  - (auth)/signup/page.tsx
  - create/page.tsx
  - page.tsx                  → Home Feed
  - post/[id]/page.tsx        → Post Detail
  - profile/[username]/page.tsx → Profile Page
- components/
  - Postcard.tsx
  - ui/ (shadcn components)
- lib/
  - auth.ts
  - db.ts
  - mongooseConnect.ts
  - utils.ts
- models/
  - Post.ts
  - UserExtension.ts
- schemas/
  - authSchema.ts
  - commentSchema.ts
  - postSchema.ts
- types/next-auth.d.ts
- middleware.ts

### Database
Use this MongoDB Atlas connection string:
mongodb+srv://astha8770194969_db_user:ircYM259UZHXJycE@instamock.r2m0bii.mongodb.net/?appName=InstaMock

Database name: InstaMock (or default to the one in connection string)

### Required Features (Implement ALL)

**1. Authentication**
- Use NextAuth.js v5 with Credentials provider + MongoDB adapter
- Signup & Login (email + password + username for signup)
- NextAuth handles password hashing automatically via adapter
- Store additional user fields (username, bio, profilePic optional) in a custom UserExtension model
- Protect all routes that require auth using middleware.ts or session checks
- On successful login/signup → redirect to home feed, store session

**2. User Model Extensions**
- Extend NextAuth user with:
  - username (unique)
  - followers: [ObjectId] (users following this user)
  - following: [ObjectId] (users this user follows)

**3. Follow System**
- API routes (app/api/follow/) for follow/unfollow
- Toggle follow/unfollow
- Update both follower and following arrays atomically

**4. Post Model**
- Fields: author (ref User), imageUrl (string), caption (string), likes: [ObjectId], comments: [{ author: ref User, text: string, createdAt }]
- Timestamps

**5. Likes & Comments**
- Authenticated users can like/unlike posts (toggle)
- Authenticated users can add comments
- Update UI instantly without refresh

**6. Feed**
- Home feed (app/page.tsx): Show posts from users the current user follows (sorted by newest)
- Include posts from followed users only

**7. Screens to Implement**

- Login & Signup pages ((auth) group)
  - Use react-hook-form + zod validation
  - Clean forms with shadcn/ui components

- Home Feed (app/page.tsx)
  - List of Postcard components
  - Each post shows: image, caption, author username/avatar, like count, comment count, like button (toggle), comment form

- Create Post (app/create/page.tsx)
  - Form: imageUrl (text input), caption (textarea)
  - Validate with zod
  - On submit → create post → redirect to home

- Profile Page (app/profile/[username]/page.tsx)
  - Show user’s posts in grid/list
  - Show follower/following counts
  - Follow/Unfollow button (if not own profile)
  - Display username, optional bio

- Post Detail (app/post/[id]/page.tsx)
  - Full view of single post
  - Large image, caption
  - List of comments with usernames
  - Like button + comment form

**8. General Frontend Requirements**
- Use Axios or Fetch for API calls (prefer Fetch)
- Optimistic UI updates where possible (likes, follows)
- State management via React context or simple useState/SWR if needed
- Responsive design with Tailwind + shadcn/ui
- Use Postcard.tsx for reusable post display
- Show loading states and error toasts (use sonner)

**9. API Routes to Create (under app/api/)**
- auth: handled by NextAuth → app/api/auth/[...nextauth]/route.ts
- posts: create, get feed
- post/[id]: get single post, like, unlike, comment
- follow: follow/unfollow
- user/[username]: get user profile data

**10. Additional Setup**
- Configure NextAuth in lib/auth.ts with MongoDB adapter
- Connect Mongoose in lib/mongooseConnect.ts (singleton pattern)
- Use the existing schemas in /schemas for form validation
- Add proper types in types/next-auth.d.ts for session.user extensions

### Instructions for You (AI)
- Implement the entire project step by step, creating/updating files within the existing structure.
- Do NOT change the folder structure.
- Write clean, readable, well-commented TypeScript code.
- Use shadcn/ui components wherever possible.
- Handle errors gracefully and show user feedback.
- Ensure all protected routes check session properly.
- Make sure feed only shows posts from followed users.
- Use populate() in Mongoose queries to get author usernames/avatars.

Start by setting up NextAuth with MongoDB adapter, then models, then API routes, then pages one by one. Prioritize authentication first, then feed, then other features.

Implement everything required for a complete, working Instagram mini clone as per the task specification.