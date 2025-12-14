"use client"

import React, { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Postcard from "@/components/Postcard";

export default function ProfilePage() {
	const params = useParams();
	const username = (params as any)?.username;
	const [loading, setLoading] = useState(true);
	const [user, setUser] = useState<any | null>(null);
	const [posts, setPosts] = useState<any[]>([]);
	const [isFollowing, setIsFollowing] = useState(false);
	const [toggling, setToggling] = useState(false);

	useEffect(() => {
		if (!username) return;
		setLoading(true);
		fetch(`/api/user/${encodeURIComponent(username)}`)
			.then((r) => r.json())
			.then((data) => {
				if (data?.user) {
					setUser(data.user);
					setPosts(data.posts || []);
					setIsFollowing(!!data.user.isFollowing);
				}
			})
			.catch(() => {})
			.finally(() => setLoading(false));
	}, [username]);

	async function toggleFollow() {
		if (!user?.userId) return;
		setToggling(true);
		try {
			const res = await fetch(`/api/follow`, {
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({ targetUserId: user.userId }),
			});
			const data = await res.json();
			if (res.ok) {
				setIsFollowing(!!data.following);
				setUser((u: any) => ({ ...u, followersCount: data.following ? (u.followersCount || 0) + 1 : Math.max(0, (u.followersCount || 1) - 1) }));
			}
		} catch (e) {
		} finally {
			setToggling(false);
		}
	}

	if (loading) return <div className="p-6">Loading...</div>;
	if (!user) return <div className="p-6">User not found</div>;

	return (
		<div className="mx-auto max-w-3xl p-6">
			<div className="flex items-center gap-4 mb-6">
				<div className="h-20 w-20 rounded-full bg-zinc-200 flex items-center justify-center text-xl">{user.username?.[0]}</div>
				<div>
					<div className="flex items-center gap-4">
						<h2 className="text-2xl font-semibold">{user.username}</h2>
						<button onClick={toggleFollow} disabled={toggling} className={`rounded px-3 py-1 ${isFollowing ? 'bg-zinc-200' : 'bg-primary text-white'}`}>
							{isFollowing ? 'Following' : 'Follow'}
						</button>
					</div>
					<div className="text-sm text-muted-foreground mt-2">{user.bio}</div>
					<div className="text-sm text-muted-foreground mt-2">{user.followersCount} followers · {user.followingCount} following</div>
				</div>
			</div>

			<div>
				<h3 className="font-semibold mb-3">Posts</h3>
				{posts.length === 0 ? (
					<div className="rounded bg-card p-6 text-muted-foreground">No posts yet</div>
				) : (
					<div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
						{posts.map((p: any) => (
							<Postcard key={p._id} post={p} />
						))}
					</div>
				)}
			</div>
		</div>
	);
}
