"use client";

import * as React from "react";
import Autoplay from "embla-carousel-autoplay";

import { OlympicsRow } from "@/types/olympics";
import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
} from "@/components/ui/carousel";

import SportManagersBarChart from "./SportManagersBarChart";
import { SPORTS } from "../shared/sports";

export default function OlympicsSportsCarousel({ rows }: { rows: OlympicsRow[] }) {
    const plugin = React.useRef(
        Autoplay({ delay: 4000, stopOnInteraction: true, stopOnMouseEnter: true })
    );

    return (
        <div className="relative">
            <Carousel
                opts={{ align: "start", loop: true }}
                plugins={[plugin.current]}
                className="w-full"
            >
                <CarouselContent>
                    {SPORTS.map((s) => (
                        <CarouselItem
                            key={String(s.key)}
                            className="basis-full md:basis-1/2 lg:basis-1/3"
                        >
                            <SportManagersBarChart
                                title={s.title}
                                type={s.type}
                                rows={rows}
                                getValue={s.getValue}
                                limit={15}
                            />
                        </CarouselItem>
                    ))}
                </CarouselContent>

                <CarouselPrevious className="-left-3" />
                <CarouselNext className="-right-3" />
            </Carousel>
        </div>
    );
}
