import { NextResponse } from "next/server";
import connectToDatabase from "../../../../../lib/mongooseConnect";
import Post from "../../../../../models/Post";

export async function GET(req: Request, { params }: { params: { id: string } }) {
  try {
    await connectToDatabase();
    const { id } = params;
    const post = await Post.findById(id).populate({ path: "author", select: "email" }).populate({ path: "comments.author", select: "email" }).lean();
    if (!post) return NextResponse.json({ error: "Not found" }, { status: 404 });
    return NextResponse.json({ post });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Failed to fetch post" }, { status: 500 });
  }
}
