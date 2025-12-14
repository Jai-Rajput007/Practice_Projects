import { MongoClient } from "mongodb";

const uri = process.env.MONGODB_URI || process.env.NEXT_PUBLIC_MONGODB || process.env.DATABASE_URL;
if (!uri) {
  throw new Error("Please define the MONGODB_URI environment variable in .env.local");
}

let client: MongoClient;
let clientPromise: Promise<MongoClient>;

declare global {
  // eslint-disable-next-line no-var
  var _mongoClientPromise: Promise<MongoClient> | undefined;
}

if (!global._mongoClientPromise) {
  client = new MongoClient(uri);
  global._mongoClientPromise = client.connect();
}

clientPromise = global._mongoClientPromise as Promise<MongoClient>;

export default clientPromise;
