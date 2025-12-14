import bcrypt from "bcrypt";
import type { NextAuthOptions } from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import connectToDatabase from "./mongooseConnect";
import mongoose from "mongoose";

export async function hashPassword(password: string) {
	const salt = await bcrypt.genSalt(10);
	return bcrypt.hash(password, salt);
}

export async function verifyPassword(password: string, hashed: string) {
	return bcrypt.compare(password, hashed);
}

// Minimal NextAuth options object (Credentials provider)
export const authOptions: NextAuthOptions = {
	providers: [
		CredentialsProvider({
			name: "Credentials",
			credentials: {
				email: { label: "Email", type: "text" },
				password: { label: "Password", type: "password" },
			},
			async authorize(credentials) {
				if (!credentials) return null;
				await connectToDatabase();
				const usersCollection = mongoose.connection.collection("users");
				const user = await usersCollection.findOne({ email: credentials.email });
				if (!user) return null;
				const valid = await verifyPassword(credentials.password, user.password as string);
				if (!valid) return null;
				// return object expected by NextAuth
				return { id: user._id.toString(), email: user.email } as any;
			},
		}),
	],
	session: { strategy: "jwt" },
};

export default authOptions;
