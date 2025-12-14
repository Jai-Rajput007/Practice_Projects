"use client"

import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useSession, signIn, signOut } from "next-auth/react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar";

type Me = { username?: string; profilePic?: string } | null;

export default function NavBar() {
  const { data: session } = useSession();
  const [me, setMe] = useState<Me | undefined>(undefined);

  useEffect(() => {
    let mounted = true;
    setMe(undefined);
    fetch("/api/me")
      .then((r) => r.json())
      .then((data) => {
        if (!mounted) return;
        setMe(data?.user ?? null);
      })
      .catch(() => setMe(null));
    return () => { mounted = false };
  }, [session]);

  return (
    <header className="w-full border-b bg-card px-6 py-3">
      <nav className="mx-auto max-w-4xl flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link href="/" className="text-xl font-semibold">Instamock</Link>
          <Link href="/create" className="text-sm text-muted-foreground">Create</Link>
        </div>

        <div className="flex items-center gap-3">
          {!session && (
            <>
              <Button variant="ghost" size="sm" onClick={() => signIn()}>Sign in</Button>
              <Link href="/auth/signup"><Button size="sm">Sign up</Button></Link>
            </>
          )}

          {session && (
            <>
              {me === undefined ? (
                <div className="flex items-center gap-2">
                  <div className="h-8 w-8 rounded-full bg-zinc-200 animate-pulse" />
                  <div className="h-4 w-24 rounded bg-zinc-200 animate-pulse" />
                </div>
              ) : (
                <Link href={`/profile/${me?.username || (session.user as any).id}`} className="flex items-center gap-2">
                  <Avatar className="h-8 w-8">
                    {me?.profilePic ? (
                      <AvatarImage src={me.profilePic} alt={me.username || (session.user as any).email} />
                    ) : (
                      <AvatarFallback>{(me?.username || (session.user as any).email || "?")[0]}</AvatarFallback>
                    )}
                  </Avatar>
                  <span className="text-sm">{me?.username || (session.user as any).email}</span>
                </Link>
              )}
              <Button variant="outline" size="sm" onClick={() => signOut()}>Sign out</Button>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
