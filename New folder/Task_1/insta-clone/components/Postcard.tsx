"use client"

import React, { useState } from "react";

type Author = { _id?: string; email?: string; username?: string; profilePic?: string };

type Comment = { _id?: string; author?: Author; text: string; createdAt?: string };

type Post = {
  _id: string;
  author: Author;
  imageUrl: string;
  caption?: string;
  likes?: string[];
  comments?: Comment[];
  createdAt?: string;
};

export default function Postcard({ post }: { post: Post }) {
  const [liked, setLiked] = useState(false);
  const [likesCount, setLikesCount] = useState(post.likes?.length || 0);

  async function toggleLike() {
    // optimistic UI update
    setLiked((v) => {
      const next = !v;
      setLikesCount((c) => (next ? c + 1 : Math.max(0, c - 1)));
      return next;
    });

    try {
      await fetch(`/api/post/${post._id}/like`, { method: "POST" });
    } catch (e) {
      // revert on error
      setLiked((v) => {
        const next = !v;
        setLikesCount((c) => (next ? c + 1 : Math.max(0, c - 1)));
        return next;
      });
    }
  }

  return (
    <article className="border rounded-md overflow-hidden bg-white shadow-sm">
      <div className="p-3 flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-zinc-200 flex items-center justify-center text-sm">{post.author?.username?.[0] ?? post.author?.email?.[0]}</div>
        <div>
          <div className="font-medium">{post.author?.username || post.author?.email}</div>
          <div className="text-xs text-muted-foreground">{new Date(post.createdAt || "").toLocaleString()}</div>
        </div>
      </div>

      <div className="w-full bg-zinc-100">
        <img src={post.imageUrl} alt={post.caption || "post image"} className="w-full object-cover max-h-[480px] mx-auto" />
      </div>

      <div className="p-3">
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-3">
            <button onClick={toggleLike} className={`px-2 py-1 rounded ${liked ? "text-red-600" : "text-zinc-700"}`}>
              {liked ? "♥" : "♡"}
            </button>
            <div className="text-sm">{likesCount} likes</div>
          </div>
          <div className="text-sm text-zinc-500">{(post.comments?.length || 0)} comments</div>
        </div>

        <div className="text-sm"><span className="font-medium mr-2">{post.author?.username || post.author?.email}</span>{post.caption}</div>
      </div>
    </article>
  );
}
