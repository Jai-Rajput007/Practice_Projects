import mongoose from "mongoose";

const MONGODB_URI = process.env.MONGODB_URI || process.env.NEXT_PUBLIC_MONGODB || process.env.DATABASE_URL || "mongodb+srv://astha8770194969_db_user:ircYM259UZHXJycE@instamock.r2m0bii.mongodb.net/InstaMock";

if (!MONGODB_URI) {
	throw new Error("Please define the MONGODB_URI environment variable inside .env.local");
}

let cached: { conn: typeof mongoose | null; promise: Promise<typeof mongoose> | null } = (global as any).mongoose || { conn: null, promise: null };

export async function connectToDatabase() {
	if (cached.conn) {
		return cached.conn;
	}

	if (!cached.promise) {
		const opts = {
			bufferCommands: false,
		} as mongoose.ConnectOptions;

		cached.promise = mongoose.connect(MONGODB_URI, opts).then((mongoose) => {
			return mongoose;
		});
	}

	cached.conn = await cached.promise;
	(global as any).mongoose = cached;
	return cached.conn;
}

export default connectToDatabase;
