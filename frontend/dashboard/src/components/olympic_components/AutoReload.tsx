"use client";

import { useEffect } from "react";

type Props = {
    intervalMs?: number;
};

export default function AutoReload({ intervalMs = 5 * 60 * 1000 }: Props) {
    useEffect(() => {
        const id = setInterval(() => {
            window.location.reload();
        }, intervalMs);

        return () => clearInterval(id);
    }, [intervalMs]);

    return null;
}