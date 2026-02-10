"use client";

import { useEffect, useState } from "react";

function formatDate(d: Date) {
    return new Intl.DateTimeFormat("ru-RU", {
        day: "numeric",
        month: "long",
        year: "numeric",
    }).format(d);
}

export default function CurrentDate() {
    const [date, setDate] = useState(() => formatDate(new Date()));

    useEffect(() => {
        const id = setInterval(() => setDate(formatDate(new Date())), 60_000);
        return () => clearInterval(id);
    }, []);

    return <>{date}</>;
}
