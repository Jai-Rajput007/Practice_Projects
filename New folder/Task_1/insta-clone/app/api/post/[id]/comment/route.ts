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

    const body = await req.json();
    const text = (body?.text || "").toString().trim();
    if (!text) return NextResponse.json({ error: "Comment text required" }, { status: 400 });

    await connectToDatabase();
    const userId = new mongoose.Types.ObjectId((session.user as any).id);

    const post = await Post.findById(params.id);
    if (!post) return NextResponse.json({ error: "Post not found" }, { status: 404 });

    post.comments.push({ author: userId, text });
    await post.save();

    const created = post.comments[post.comments.length - 1];
    return NextResponse.json({ comment: created }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Error adding comment" }, { status: 500 });
  }
}
