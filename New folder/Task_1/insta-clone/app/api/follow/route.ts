import { NextResponse } from "next/server";
import connectToDatabase from "../../../lib/mongooseConnect";
import UserExtension from "../../../models/UserExtension";
import { getServerSession } from "next-auth";
import authOptions from "../../../lib/auth";
import mongoose from "mongoose";

export async function POST(req: Request) {
  try {
    const session = await getServerSession(authOptions as any);
    if (!session || !(session.user as any).id) return NextResponse.json({ error: "Unauthorized" }, { status: 401 });

    const body = await req.json();
    const targetId = body?.targetUserId;
    if (!targetId) return NextResponse.json({ error: "targetUserId required" }, { status: 400 });

    await connectToDatabase();

    const meId = new mongoose.Types.ObjectId((session.user as any).id);
    const targetObjId = new mongoose.Types.ObjectId(targetId);

    const target = await UserExtension.findOne({ userId: targetObjId });
    const me = await UserExtension.findOne({ userId: meId });
    if (!target || !me) return NextResponse.json({ error: "User not found" }, { status: 404 });

    const isFollowing = (me.following || []).some((f) => f.toString() === targetObjId.toString());

    if (isFollowing) {
      // unfollow
      await UserExtension.updateOne({ userId: meId }, { $pull: { following: targetObjId } });
      await UserExtension.updateOne({ userId: targetObjId }, { $pull: { followers: meId } });
      return NextResponse.json({ ok: true, following: false });
    } else {
      await UserExtension.updateOne({ userId: meId }, { $addToSet: { following: targetObjId } });
      await UserExtension.updateOne({ userId: targetObjId }, { $addToSet: { followers: meId } });
      return NextResponse.json({ ok: true, following: true });
    }
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Follow error" }, { status: 500 });
  }
}
