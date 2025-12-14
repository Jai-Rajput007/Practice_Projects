import mongoose, { Schema, Document, Model } from "mongoose";
import connectToDatabase from "../lib/mongooseConnect";

export interface IUserExtension extends Document {
	userId: mongoose.Types.ObjectId;
	username: string;
	bio?: string;
	profilePic?: string;
	followers: mongoose.Types.ObjectId[];
	following: mongoose.Types.ObjectId[];
}

const UserExtensionSchema = new Schema<IUserExtension>(
	{
		userId: { type: Schema.Types.ObjectId, required: true, ref: "User", unique: true },
		username: { type: String, required: true, unique: true },
		bio: { type: String, default: "" },
		profilePic: { type: String, default: "" },
		followers: [{ type: Schema.Types.ObjectId, ref: "User" }],
		following: [{ type: Schema.Types.ObjectId, ref: "User" }],
	},
	{ timestamps: true }
);

let UserExtension: Model<IUserExtension>;

try {
	// Ensure DB connection
	connectToDatabase();
} catch (e) {
	// ignore during type-only or build time
}

try {
	UserExtension = mongoose.model<IUserExtension>("UserExtension");
} catch (e) {
	UserExtension = mongoose.model<IUserExtension>("UserExtension", UserExtensionSchema);
}

export default UserExtension;
