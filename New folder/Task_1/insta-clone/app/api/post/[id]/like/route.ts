import { NextResponse } from "next/server";
import connectToDatabase from "../../../../../lib/mongooseConnect";
import Post from "../../../../../models/Post";
import { getServerSession } from "next-auth";
import authOptions from "../../../../../lib/auth";
import mongoose from "mongoose";

export async function POST(req: Request, { params }: { params: { id: string } }) {
  try {
    const session = await getServerSession(authOptions as any);
    if (!session || !(session.user as any).id) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    await connectToDatabase();
    const userId = new mongoose.Types.ObjectId((session.user as any).id);
    const postId = params.id;

    const post = await Post.findById(postId);
    if (!post) return NextResponse.json({ error: "Post not found" }, { status: 404 });

    const hasLiked = post.likes.some((l) => l.toString() === userId.toString());
    if (hasLiked) {
      post.likes = post.likes.filter((l) => l.toString() !== userId.toString());
    } else {
      post.likes.push(userId);
    }

    await post.save();

    return NextResponse.json({ likes: post.likes.length, liked: !hasLiked });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Error toggling like" }, { status: 500 });
  }
}
