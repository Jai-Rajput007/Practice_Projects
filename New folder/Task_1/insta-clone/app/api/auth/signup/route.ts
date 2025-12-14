import { NextResponse } from "next/server";
import { signupSchema } from "../../../../schemas/authSchema";
import { hashPassword } from "../../../../lib/auth";
import connectToDatabase from "../../../../lib/mongooseConnect";
import mongoose from "mongoose";
import UserExtension from "../../../../models/UserExtension";

export async function POST(req: Request) {
  try {
    const body = await req.json();
    const parsed = signupSchema.safeParse(body);
    if (!parsed.success) {
      return NextResponse.json({ error: parsed.error.errors }, { status: 400 });
    }

    const { email, password, username } = parsed.data as any;

    await connectToDatabase();

    const users = mongoose.connection.collection("users");

    const existingEmail = await users.findOne({ email });
    if (existingEmail) {
      return NextResponse.json({ error: "Email already in use" }, { status: 409 });
    }

    const existingUsername = await UserExtension.findOne({ username });
    if (existingUsername) {
      return NextResponse.json({ error: "Username already taken" }, { status: 409 });
    }

    const hashed = await hashPassword(password);

    const result = await users.insertOne({ email, password: hashed, emailVerified: null });

    await UserExtension.create({ userId: result.insertedId, username, bio: "", profilePic: "", followers: [], following: [] });

    return NextResponse.json({ ok: true }, { status: 201 });
  } catch (err: any) {
    return NextResponse.json({ error: err?.message || "Internal error" }, { status: 500 });
  }
}
