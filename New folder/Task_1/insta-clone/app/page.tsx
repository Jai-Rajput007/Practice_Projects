"use client"

import React, { useEffect, useState } from "react";
import Postcard from "@/components/Postcard";

type Post = any;

export default function Home() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("/api/posts")
      .then((r) => r.json())
      .then((data) => {
        if (data?.posts) setPosts(data.posts);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="mx-auto max-w-3xl p-6">
      <h1 className="text-2xl font-semibold mb-4">Home Feed</h1>
      {loading ? (
        <div>Loading feed...</div>
      ) : posts.length === 0 ? (
        <div className="text-muted-foreground">No posts to show. Follow users to see their posts.</div>
      ) : (
        <div className="space-y-6">
          {posts.map((p: Post) => (
            <Postcard key={p._id} post={p} />
          ))}
        </div>
      )}
    </div>
  );
}
