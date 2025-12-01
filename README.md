Travel Planner — Multi-Agent AI System (Phase 1)

A full multi-agent AI travel planning system built using LangGraph, custom tools, and external APIs.
This project generates geocoding, weather forecasts, nearby attractions, distance matrices, and a day-wise itinerary using a coordinated multi-agent workflow.

This is Phase 1, providing a fully working end-to-end pipeline.

Key Features
1. Multi-Agent Architecture

The system contains three major agents, each with a clear role:

Agent	Responsibility
Budget Agent	Estimates total trip cost, checks affordability, suggests alternatives
Places Agent	Fetches attractions, beaches, food spots using Geoapify
Routing Agent	Builds road-distance & time matrix using OpenRouteService
Itinerary Agent (LLM)	Generates final travel itinerary using Groq LLM

These agents coordinate through a LangGraph workflow.

2. Tool Integrations
Tool	Purpose
Geoapify Places API	Attractions, beaches, food spots
Open-Meteo Weather API	7-day weather forecast
OpenRouteService Matrix API	Drive distances & times
Nominatim (OpenStreetMap)	Geocoding (lat/lon lookup)

3. Orchestration — LangGraph
The entire workflow is managed using a LangGraph graph-based pipeline, with sequential nodes:
geocode
weather
places
routing
budget
itinerary
This ensures agents work in a deterministic order and pass state correctly.

4. Final Output
Running the system produces:
Geocoded destination
Weather forecast
45+ places (attractions/beaches/food)
Routing matrix
Budget calculation
Full AI-generated markdown itinerary

Project Structure
travel_planner_proj/
│
├── travel_planner.py
├── src/
│   ├── agents/
│   │   ├── budget_agent.py
│   │   ├── places_agent.py
│   │   ├── routing_agent.py
│   │   └── itinerary_agent.py
│   │
│   ├── tools/
│   │   ├── geocode.py
│   │   ├── weather.py
│   │   ├── places.py
│   │   ├── routing_matrix.py
│   │   └── pricing_model.py
│   │
│   └── workflow/
│       ├── state.py
│       ├── graph.py
│       └── nodes/
│           ├── geocode_node.py
│           ├── weather_node.py
│           ├── places_node.py
│           ├── routing_node.py
│           ├── budget_node.py
│           └── itinerary_node.py
│
└── README.md

Phase 2 — Coming Next
Here’s what we will add next:
 Human-in-the-loop approval
 MCP-based tool access
 LangGraph memory + checkpointing
 UI (Streamlit / FastAPI)
 Real hotel + flight price APIs (free or simulated)
 Save itineraries / export PDF
