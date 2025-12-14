import mongoose, { Schema, Document, Model } from "mongoose";
import connectToDatabase from "../lib/mongooseConnect";

export interface IComment {
	author: mongoose.Types.ObjectId;
	text: string;
	createdAt?: Date;
}

export interface IPost extends Document {
	author: mongoose.Types.ObjectId;
	imageUrl: string;
	caption?: string;
	likes: mongoose.Types.ObjectId[];
	comments: IComment[];
	createdAt?: Date;
	updatedAt?: Date;
}

const CommentSchema = new Schema<IComment>(
	{
		author: { type: Schema.Types.ObjectId, ref: "User", required: true },
		text: { type: String, required: true },
	},
	{ timestamps: { createdAt: true, updatedAt: false } }
);

const PostSchema = new Schema<IPost>(
	{
		author: { type: Schema.Types.ObjectId, ref: "User", required: true },
		imageUrl: { type: String, required: true },
		caption: { type: String, default: "" },
		likes: [{ type: Schema.Types.ObjectId, ref: "User" }],
		comments: [CommentSchema],
	},
	{ timestamps: true }
);

let Post: Model<IPost>;

try {
	connectToDatabase();
} catch (e) {}

try {
	Post = mongoose.model<IPost>("Post");
} catch (e) {
	Post = mongoose.model<IPost>("Post", PostSchema);
}

export default Post;
