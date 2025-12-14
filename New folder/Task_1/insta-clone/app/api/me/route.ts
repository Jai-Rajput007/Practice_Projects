import { NextResponse } from "next/server";
import { getServerSession } from "next-auth";
import authOptions from "../../../lib/auth";
import connectToDatabase from "../../../lib/mongooseConnect";
import UserExtension from "../../../models/UserExtension";

export async function GET() {
  try {
    const session = await getServerSession(authOptions as any);
    if (!session || !(session.user as any).id) return NextResponse.json({ user: null });

    await connectToDatabase();

    const ext = await UserExtension.findOne({ userId: (session.user as any).id }).lean();
    if (!ext) return NextResponse.json({ user: null });

    return NextResponse.json({
      user: {
        username: ext.username,
        bio: ext.bio,
        profilePic: ext.profilePic,
        followersCount: (ext.followers || []).length,
        followingCount: (ext.following || []).length,
        userId: ext.userId?.toString(),
      },
    });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Failed" }, { status: 500 });
  }
}
