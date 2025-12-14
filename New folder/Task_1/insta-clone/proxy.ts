// Temporary minimal proxy/middleware to satisfy Next.js requirement.
// Next.js 16 deprecates `middleware`; consider renaming this file to `proxy.ts`
// or removing it if middleware behavior is not needed.

import { NextResponse } from 'next/server';

export default function middleware(request: Request) {
	return NextResponse.next();
}
