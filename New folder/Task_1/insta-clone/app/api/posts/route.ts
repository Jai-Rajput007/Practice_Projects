import { NextResponse } from "next/server";
import connectToDatabase from "../../../../lib/mongooseConnect";
import Post from "../../../../models/Post";
import UserExtension from "../../../../models/UserExtension";
import mongoose from "mongoose";
import { getServerSession } from "next-auth";
import authOptions from "../../../../lib/auth";
import { createPostSchema } from "../../../../schemas/postSchema";

export async function GET() {
  try {
    await connectToDatabase();

    // Note: we cannot access the request to get session in this simple handler,
    // but getServerSession reads cookies from the runtime.
    const session = await getServerSession(authOptions as any);
    let followingIds: mongoose.Types.ObjectId[] = [];

    if (session && session.user && (session.user as any).id) {
      const ext = await UserExtension.findOne({ userId: (session.user as any).id });
      if (ext) {
        followingIds = ext.following || [];
      }
    }

    // include own posts as well
    const authors = [...followingIds];
    if (session && (session.user as any).id) {
      authors.push(new mongoose.Types.ObjectId((session.user as any).id));
    }

    const posts = await Post.find({ author: { $in: authors } })
      .sort({ createdAt: -1 })
      .populate({ path: "author", select: "email" })
      .populate({ path: "comments.author", select: "email" })
      .lean();

    return NextResponse.json({ posts });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Failed to get posts" }, { status: 500 });
  }
}

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const parsed = createPostSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.errors }, { status: 400 });
    }

    const session = await getServerSession(authOptions as any);
    if (!session || !(session.user as any).id) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    await connectToDatabase();

    const created = await Post.create({ author: (session.user as any).id, ...parsed.data });

    return NextResponse.json({ post: created }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Failed to create post" }, { status: 500 });
  }
}
