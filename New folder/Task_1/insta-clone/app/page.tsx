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
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-semibold">Home Feed</h1>
      </div>

      {loading ? (
        <div className="space-y-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="rounded bg-card p-6 animate-pulse">&nbsp;</div>
          ))}
        </div>
      ) : posts.length === 0 ? (
        <div className="rounded bg-card p-6 text-muted-foreground">No posts to show. Follow users to see their posts.</div>
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
