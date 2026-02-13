"use client";

import * as React from "react";
import Autoplay from "embla-carousel-autoplay";

import type { OlympicsTeamAgg } from "@/types/olympics";
import { SPORTS } from "../shared/sports";

import {
    Carousel,
    CarouselContent,
    CarouselItem,
    CarouselNext,
    CarouselPrevious,
} from "@/components/ui/carousel";

import SportTeamsVerticalBarChart from "./SportTeamsVerticalBarChart";

export default function OlympicsTeamsCarousel({ teams }: { teams: OlympicsTeamAgg[] }) {
    const plugin = React.useRef(
        Autoplay({ delay: 4500, stopOnInteraction: true, stopOnMouseEnter: true })
    );
    const safeTeams = Array.isArray(teams) ? teams : [];



    return (
        <div className="relative">
            <Carousel opts={{ align: "start", loop: true }} plugins={[plugin.current]} className="w-full">
                <CarouselContent>
                    {SPORTS.map((s) => (
                        <CarouselItem key={String(s.key)} className="basis-full md:basis-1/2 lg:basis-1/5">
                            <SportTeamsVerticalBarChart
                                title={s.title}
                                type={s.type}
                                teams={teams}
                                metricKey={s.key as keyof OlympicsTeamAgg}
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
