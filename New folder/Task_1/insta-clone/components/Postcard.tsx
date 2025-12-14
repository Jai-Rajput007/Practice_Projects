"use client"

import React, { useState } from "react";
import Image from "next/image";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

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
  const [comments, setComments] = useState<Comment[]>(post.comments || []);
  const [commentText, setCommentText] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function toggleLike() {
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

  async function submitComment(e?: React.FormEvent) {
    e?.preventDefault();
    if (!commentText.trim()) return;
    setSubmitting(true);

    // optimistic add
    const optimistic: Comment = { _id: `temp-${Date.now()}`, text: commentText.trim(), author: { username: "You" }, createdAt: new Date().toISOString() };
    setComments((c) => [...c, optimistic]);
    setCommentText("");

    try {
      const res = await fetch(`/api/post/${post._id}/comment`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ text: optimistic.text }) });
      const data = await res.json();
      if (!res.ok) {
        // remove optimistic
        setComments((c) => c.filter((x) => x._id !== optimistic._id));
      } else {
        // replace optimistic with server comment if provided
        if (data?.comment) {
          setComments((c) => c.map((x) => (x._id === optimistic._id ? data.comment : x)));
        }
      }
    } catch (err) {
      setComments((c) => c.filter((x) => x._id !== optimistic._id));
    } finally {
      setSubmitting(false);
    }
  }

  const [imgLoaded, setImgLoaded] = useState(false);

  return (
    <Card className="overflow-hidden transition hover:shadow-lg hover:-translate-y-0.5 transform">
      <div className="p-3 flex items-center gap-3">
        <Avatar className="h-10 w-10">
          {post.author?.profilePic ? (
            <AvatarImage src={post.author.profilePic} alt={post.author?.username || post.author?.email} />
          ) : (
            <AvatarFallback>{(post.author?.username || post.author?.email || "?")[0]}</AvatarFallback>
          )}
        </Avatar>
        <div>
          <div className="font-medium">{post.author?.username || post.author?.email}</div>
          <div className="text-xs text-muted-foreground">{post.createdAt ? new Date(post.createdAt).toLocaleString() : ""}</div>
        </div>
      </div>

      <CardContent className="p-0">
        <div className="w-full bg-zinc-100 relative" style={{ minHeight: 220 }}>
          {!imgLoaded && <div className="absolute inset-0 animate-pulse bg-zinc-200" />}
          <Image
            src={post.imageUrl}
            alt={post.caption || "post image"}
            fill
            className={`object-cover mx-auto transition-transform duration-300 ${imgLoaded ? 'scale-100' : 'scale-105'}`}
            onLoadingComplete={() => setImgLoaded(true)}
            loading="lazy"
            unoptimized
          />
        </div>
      </CardContent>

      <CardFooter>
        <div className="w-full">
          <div className="flex items-center justify-between mb-2">
            <div className="flex items-center gap-3">
              <Button variant="ghost" size="sm" onClick={toggleLike}>{liked ? '♥' : '♡'}</Button>
              <div className="text-sm">{likesCount} likes</div>
            </div>
            <div className="text-sm text-muted-foreground">{comments.length} comments</div>
          </div>

          <div className="text-sm mb-3"><span className="font-medium mr-2">{post.author?.username || post.author?.email}</span>{post.caption}</div>

          <div className="space-y-2">
            {comments.map((c) => (
              <div key={c._id} className="text-sm border-t pt-2">
                <span className="font-medium mr-2">{c.author?.username || c.author?.email || "User"}</span>
                <span>{c.text}</span>
              </div>
            ))}
          </div>

          <form onSubmit={submitComment} className="mt-3 flex gap-2">
            <input value={commentText} onChange={(e) => setCommentText(e.target.value)} placeholder="Add a comment..." className="flex-1 rounded border px-3 py-2" />
            <Button type="submit" size="sm" disabled={submitting}>Post</Button>
          </form>
        </div>
      </CardFooter>
    </Card>
  );
}
