import { NextResponse } from "next/server";
import connectToDatabase from "../../../../../lib/mongooseConnect";
import UserExtension from "../../../../../models/UserExtension";
import Post from "../../../../../models/Post";
import { getServerSession } from "next-auth";
import authOptions from "../../../../../lib/auth";
import mongoose from "mongoose";

export async function GET(req: Request, { params }: { params: { username: string } }) {
  try {
    const { username } = params;
    await connectToDatabase();

    const userExt = await UserExtension.findOne({ username }).lean();
    if (!userExt) return NextResponse.json({ error: "User not found" }, { status: 404 });

    const posts = await Post.find({ author: userExt.userId }).sort({ createdAt: -1 }).lean();

    // determine if requester follows this user
    let isFollowing = false;
    const session = await getServerSession(authOptions as any);
    if (session && (session.user as any).id) {
      const meId = new mongoose.Types.ObjectId((session.user as any).id);
      isFollowing = (userExt.followers || []).some((f: any) => f.toString() === meId.toString());
    }

    return NextResponse.json({
      user: {
        username: userExt.username,
        bio: userExt.bio,
        profilePic: userExt.profilePic,
        followersCount: (userExt.followers || []).length,
        followingCount: (userExt.following || []).length,
        userId: userExt.userId?.toString(),
        isFollowing,
      },
      posts,
    });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Failed to fetch user" }, { status: 500 });
  }
}
