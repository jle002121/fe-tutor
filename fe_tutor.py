#!/usr/bin/env python3
"""
FE Mechanical Exam Tutor
Teaches, quizzes, and tracks progress toward passing the NCEES FE Mechanical exam.
Run with: python3 fe_tutor.py
"""

import json
import time
import datetime
import os
import sys
import textwrap
import random

# ─────────────────────────── Constants ────────────────────────────────────────
STUDY_START = datetime.date(2026, 6, 9)
DEFAULT_EXAM_DATE = "2026-08-25"
WEEKLY_HOUR_TARGET = 13
WIDTH = 70

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROBLEMS_FILE = os.path.join(SCRIPT_DIR, "problems.json")
PROGRESS_FILE = os.path.join(SCRIPT_DIR, "progress.json")
CONFIG_FILE = os.path.join(SCRIPT_DIR, "config.json")

# ─────────────────────────── Topic Definitions ────────────────────────────────
TOPICS = [
    {
        "id": 1,
        "name": "Mathematics",
        "q_range": "6–9",
        "handbook_page": 36,
        "baseline": "strong",
        "week": 1,
        "subtopics": ["Analytic Geometry", "Calculus", "ODEs", "Linear Algebra", "Numerical Methods", "Algorithm/Logic"],
        "key_concepts": [
            {
                "title": "Derivatives and Integrals",
                "explanation": (
                    "The FE exam tests derivatives and integrals of common functions.\n"
                    "You will NOT derive from first principles — know the rules and look up tables.\n\n"
                    "Key rules:\n"
                    "  d/dx[xⁿ] = nxⁿ⁻¹          d/dx[eˣ] = eˣ\n"
                    "  d/dx[sin x] = cos x         d/dx[ln x] = 1/x\n"
                    "  ∫xⁿ dx = xⁿ⁺¹/(n+1) + C    ∫eˣ dx = eˣ + C\n\n"
                    "Handbook: p.36 — Differential Calculus and Integral Calculus tables.\n"
                    "TI-36X Pro tip: Use the numeric derivative/integral keys for verification."
                ),
                "handbook_page": 36
            },
            {
                "title": "Ordinary Differential Equations",
                "explanation": (
                    "First-order linear ODE:  dy/dx + P(x)y = Q(x)\n"
                    "Solution: y·e^(∫P dx) = ∫Q·e^(∫P dx) dx + C\n\n"
                    "For constant coefficients (most common on FE):\n"
                    "  dy/dx + ay = 0  →  y = Ce^(-ax)\n\n"
                    "Second-order: y'' + by' + cy = 0\n"
                    "Characteristic equation: r² + br + c = 0\n"
                    "  Two real roots r₁, r₂: y = C₁e^(r₁x) + C₂e^(r₂x)\n"
                    "  Repeated root r:        y = (C₁ + C₂x)e^(rx)\n"
                    "  Complex roots a±bj:     y = e^(ax)[C₁cos(bx) + C₂sin(bx)]\n\n"
                    "Handbook: p.36 — Differential equations table."
                ),
                "handbook_page": 36
            },
            {
                "title": "Laplace Transforms",
                "explanation": (
                    "Laplace transforms convert ODEs into algebraic equations.\n"
                    "Key pairs (memorize these — also in handbook p.36):\n\n"
                    "  L{1}      = 1/s\n"
                    "  L{t}      = 1/s²\n"
                    "  L{e^(at)} = 1/(s-a)\n"
                    "  L{sin(ωt)}= ω/(s²+ω²)\n"
                    "  L{cos(ωt)}= s/(s²+ω²)\n\n"
                    "Strategy: Transform → solve algebraically → inverse transform.\n"
                    "Handbook: p.36 — Laplace transform pairs and properties table."
                ),
                "handbook_page": 36
            },
            {
                "title": "Matrix Operations",
                "explanation": (
                    "For the FE exam, know:\n"
                    "  det([[a,b],[c,d]]) = ad - bc\n"
                    "  Matrix multiply: row × column dot products\n"
                    "  Cramer's rule for solving 2×2 and 3×3 systems\n\n"
                    "TI-36X Pro: 2nd → MATRIX → edit → compute.\n"
                    "Use the matrix solver for simultaneous equations in statics/circuits.\n\n"
                    "Handbook: p.36 — Linear algebra, matrix operations."
                ),
                "handbook_page": 36
            }
        ]
    },
    {
        "id": 2,
        "name": "Probability and Statistics",
        "q_range": "4–6",
        "handbook_page": 64,
        "baseline": "moderate",
        "week": 1,
        "subtopics": ["Probability Distributions", "Measures of Central Tendency", "Expected Value", "Regression"],
        "key_concepts": [
            {
                "title": "Normal Distribution and Z-Scores",
                "explanation": (
                    "z = (x - μ) / σ\n\n"
                    "Empirical rule (68-95-99.7):\n"
                    "  ±1σ → 68% of data\n"
                    "  ±2σ → 95% of data\n"
                    "  ±3σ → 99.7% of data\n\n"
                    "Use z-table in handbook (p.64) to find probabilities.\n"
                    "TI-36X Pro: STAT → 1-Var → enter data → mean and std dev auto-computed.\n\n"
                    "Handbook: p.64 — Normal distribution table, z-score formula."
                ),
                "handbook_page": 64
            },
            {
                "title": "Sample Statistics",
                "explanation": (
                    "Mean: x̄ = Σxᵢ/n\n"
                    "Sample std dev: s = √[Σ(xᵢ-x̄)²/(n-1)]  ← note (n-1) for sample\n"
                    "Population std dev: σ = √[Σ(xᵢ-μ)²/n]\n\n"
                    "Median: middle value (sort first; average two middle for even n)\n"
                    "Mode: most frequent value\n\n"
                    "Handbook: p.64 — Measures of central tendency and dispersion."
                ),
                "handbook_page": 64
            },
            {
                "title": "Linear Regression",
                "explanation": (
                    "Regression line: y = a + bx\n"
                    "Slope: b = [nΣxy - ΣxΣy] / [nΣx² - (Σx)²]\n"
                    "Intercept: a = ȳ - bx̄\n\n"
                    "Correlation coefficient r (-1 to +1):\n"
                    "  r close to ±1: strong linear relationship\n"
                    "  r close to 0: weak relationship\n\n"
                    "TI-36X Pro: DATA → enter (x,y) pairs → STAT → LinReg → reads out a, b, r.\n\n"
                    "Handbook: p.64 — Regression, linear curve fitting."
                ),
                "handbook_page": 64
            }
        ]
    },
    {
        "id": 3,
        "name": "Ethics and Professional Practice",
        "q_range": "4–6",
        "handbook_page": 4,
        "baseline": "strong",
        "week": 9,
        "subtopics": ["Codes of Ethics", "Public Health/Safety/Welfare", "Intellectual Property", "Societal Considerations"],
        "key_concepts": [
            {
                "title": "The Hierarchy — Public Welfare First",
                "explanation": (
                    "The NCEES Model Law establishes a clear priority order:\n"
                    "  1. PUBLIC HEALTH, SAFETY, AND WELFARE — always paramount\n"
                    "  2. Professional obligations to clients\n"
                    "  3. Business interests\n\n"
                    "When in doubt on any ethics question: choose the option that\n"
                    "protects public safety, even if it conflicts with client wishes.\n\n"
                    "Handbook: p.4 — NCEES Model Law and Model Rules."
                ),
                "handbook_page": 4
            },
            {
                "title": "Competence and Conflicts of Interest",
                "explanation": (
                    "Key rules you must know:\n"
                    "  • Only practice in areas where you are competent\n"
                    "  • Disclose conflicts of interest — don't hide them\n"
                    "  • Do not accept gifts that could influence your judgment\n"
                    "  • Engineers may not sign/seal work outside their competence\n\n"
                    "Intellectual property:\n"
                    "  Patent: public disclosure, 20-year protection\n"
                    "  Trade secret: confidential, no disclosure required\n"
                    "  Copyright: original creative works, automatic\n"
                    "  Trademark: brand identifiers\n\n"
                    "Handbook: p.4 — NCEES Model Rules."
                ),
                "handbook_page": 4
            },
            {
                "title": "Sustainable Design and Life-Cycle Analysis",
                "explanation": (
                    "Life-cycle analysis (LCA) evaluates environmental impact\n"
                    "from 'cradle to grave':\n"
                    "  Raw material extraction → Manufacturing → Use → Disposal\n\n"
                    "Engineers should:\n"
                    "  • Inform clients of more sustainable options\n"
                    "  • Consider long-term societal impacts\n"
                    "  • Balance economic, environmental, and social factors\n\n"
                    "Ethics questions are usually common sense. The answer that\n"
                    "protects the public and promotes transparency is almost always right.\n\n"
                    "Handbook: p.4 — Societal considerations section."
                ),
                "handbook_page": 4
            }
        ]
    },
    {
        "id": 4,
        "name": "Engineering Economics",
        "q_range": "4–6",
        "handbook_page": 235,
        "baseline": "weak",
        "week": 9,
        "subtopics": ["Time Value of Money", "Cost Types", "Economic Analyses"],
        "key_concepts": [
            {
                "title": "Interest Factor Notation — Never Memorize, Always Look Up",
                "explanation": (
                    "Five core factors (look up in handbook p.235 tables):\n\n"
                    "  (P/F, i%, n): Present worth of a future sum\n"
                    "    P = F × (P/F, i%, n) = F/(1+i)ⁿ\n\n"
                    "  (F/P, i%, n): Future worth of present sum\n"
                    "    F = P × (F/P, i%, n) = P(1+i)ⁿ\n\n"
                    "  (A/P, i%, n): Uniform payment from present sum (capital recovery)\n"
                    "    A = P × (A/P, i%, n)\n\n"
                    "  (P/A, i%, n): Present worth of uniform series\n"
                    "    P = A × (P/A, i%, n)\n\n"
                    "  (F/A, i%, n): Future worth of uniform series\n"
                    "    F = A × (F/A, i%, n)\n\n"
                    "Handbook: p.235 — Interest factor tables for all i and n values."
                ),
                "handbook_page": 235
            },
            {
                "title": "Cost Types and Decision Rules",
                "explanation": (
                    "Fixed costs: constant regardless of output (rent, equipment)\n"
                    "Variable costs: change with output (materials, labor)\n"
                    "Sunk costs: already spent — IRRELEVANT to future decisions\n"
                    "Incremental cost: additional cost from one extra unit\n"
                    "Marginal cost: derivative of total cost\n\n"
                    "Key decision rule: SUNK COSTS DO NOT MATTER.\n"
                    "If a question asks about a past investment, ignore it.\n"
                    "Only future costs and benefits are relevant.\n\n"
                    "Handbook: p.235 — Cost types."
                ),
                "handbook_page": 235
            },
            {
                "title": "Economic Analysis Methods",
                "explanation": (
                    "Present Worth (PW) method:\n"
                    "  Convert all cash flows to present value; higher PW wins.\n\n"
                    "Annual Worth (AW) method:\n"
                    "  Convert all to uniform annual cost/benefit.\n\n"
                    "Benefit-Cost Ratio: BCR = PW(Benefits)/PW(Costs)\n"
                    "  BCR > 1: justified     BCR < 1: not justified\n\n"
                    "Break-even: find the output where Revenue = Cost\n\n"
                    "IRR: the interest rate that makes NPW = 0\n"
                    "  Accept if IRR > MARR (minimum attractive rate of return)\n\n"
                    "Handbook: p.235 — Economic analysis methods."
                ),
                "handbook_page": 235
            }
        ]
    },
    {
        "id": 5,
        "name": "Electricity and Magnetism",
        "q_range": "5–8",
        "handbook_page": 270,
        "baseline": "weak",
        "week": 8,
        "subtopics": ["Electrical Fundamentals", "DC Circuit Analysis", "AC Circuit Analysis", "Motors and Generators"],
        "key_concepts": [
            {
                "title": "DC Circuit Fundamentals",
                "explanation": (
                    "Ohm's Law: V = IR\n"
                    "Power: P = IV = I²R = V²/R  (know all three forms)\n\n"
                    "Series resistors: R_eq = R₁ + R₂ + R₃\n"
                    "Parallel resistors: 1/R_eq = 1/R₁ + 1/R₂ + 1/R₃\n\n"
                    "KVL (Kirchhoff's Voltage Law):\n"
                    "  Sum of voltage drops around any closed loop = 0\n\n"
                    "KCL (Kirchhoff's Current Law):\n"
                    "  Sum of currents into a node = sum of currents out\n\n"
                    "TI-36X Pro: Use matrix solver for simultaneous KVL/KCL equations.\n\n"
                    "Handbook: E&M section — Ohm's law, KVL, KCL."
                ),
                "handbook_page": 270
            },
            {
                "title": "AC Circuits — Impedance",
                "explanation": (
                    "Impedance Z (complex resistance):\n"
                    "  Resistor: Z_R = R\n"
                    "  Inductor: Z_L = jωL = j2πfL   (X_L = ωL)\n"
                    "  Capacitor: Z_C = 1/(jωC) = -j/(ωC)  (X_C = 1/ωC)\n\n"
                    "Series impedance: Z_total = Z_R + Z_L + Z_C\n"
                    "  |Z| = √(R² + (X_L - X_C)²)\n\n"
                    "Resonance: X_L = X_C → Z = R (purely resistive)\n\n"
                    "Power factor: PF = cos(θ) = R/|Z|\n\n"
                    "Handbook: E&M section — AC circuits, phasor diagrams."
                ),
                "handbook_page": 270
            },
            {
                "title": "Motors and Generators",
                "explanation": (
                    "Motor efficiency: η = P_mechanical_out / P_electrical_in\n"
                    "  P_out = T × ω  (torque × angular velocity)\n"
                    "  P_in  = V × I × power factor\n\n"
                    "Back-EMF: as motor spins, it generates a voltage opposing supply\n"
                    "  V_supply = Back-EMF + I×R_armature\n\n"
                    "Generator: mechanical energy → electrical energy\n"
                    "  η = P_electrical_out / P_mechanical_in\n\n"
                    "These are often straightforward efficiency calculations.\n"
                    "Handbook: E&M section — motors, generators, power."
                ),
                "handbook_page": 270
            }
        ]
    },
    {
        "id": 6,
        "name": "Statics",
        "q_range": "9–14",
        "handbook_page": 95,
        "baseline": "strong",
        "week": 2,
        "subtopics": ["Resultants", "Concurrent Forces", "Equilibrium", "Trusses", "Centroids/MOI", "Friction"],
        "key_concepts": [
            {
                "title": "Free Body Diagrams and Equilibrium",
                "explanation": (
                    "The FBD is everything. Draw it before touching numbers.\n\n"
                    "2D Equilibrium conditions:\n"
                    "  ΣFx = 0    ΣFy = 0    ΣM_any_point = 0\n\n"
                    "Strategy: choose moment point to eliminate unknowns.\n"
                    "  Take moments about a pin/support to eliminate that reaction.\n\n"
                    "For a simply supported beam:\n"
                    "  Take moments about left support → solve for right reaction\n"
                    "  Use ΣFy = 0 → solve for left reaction\n\n"
                    "Handbook: p.95 — Statics, free body diagrams."
                ),
                "handbook_page": 95
            },
            {
                "title": "Trusses — Method of Joints",
                "explanation": (
                    "Truss assumptions: members are two-force members (axial only).\n\n"
                    "Method of Joints:\n"
                    "  1. Find external reactions first (FBD of whole truss)\n"
                    "  2. Start at a joint with only 2 unknowns\n"
                    "  3. ΣFx = 0, ΣFy = 0 at that joint\n"
                    "  4. Move to next joint with 2 unknowns\n\n"
                    "Method of Sections:\n"
                    "  Cut through 3 members, isolate one side, apply equilibrium.\n"
                    "  Faster when you need one specific member force.\n\n"
                    "Sign convention: Tension (+), Compression (-)\n\n"
                    "Handbook: p.95 — Trusses."
                ),
                "handbook_page": 95
            },
            {
                "title": "Centroids and Moments of Inertia",
                "explanation": (
                    "Standard shapes — look up in handbook table (p.95):\n\n"
                    "  Rectangle: centroid at (b/2, h/2), I_x = bh³/12\n"
                    "  Triangle: centroid at h/3 from base, I_x = bh³/36\n"
                    "  Circle: centroid at center, I = πr⁴/4 = πd⁴/64\n"
                    "  Semicircle: centroid at 4r/3π from diameter\n\n"
                    "Parallel axis theorem: I = I_centroid + Ad²\n"
                    "  (shift MOI from centroid to any parallel axis)\n\n"
                    "Composite area: divide into simple shapes, apply parallel axis.\n\n"
                    "Handbook: p.95 — Geometric properties table."
                ),
                "handbook_page": 95
            }
        ]
    },
    {
        "id": 7,
        "name": "Dynamics, Kinematics, and Vibrations",
        "q_range": "10–15",
        "handbook_page": 102,
        "baseline": "strong",
        "week": 3,
        "subtopics": ["Particle Kinematics", "Newton's 2nd Law", "Work-Energy", "Impulse-Momentum", "Rigid Bodies", "Vibrations"],
        "key_concepts": [
            {
                "title": "Constant Acceleration Kinematics",
                "explanation": (
                    "Four equations (for constant acceleration):\n\n"
                    "  v = v₀ + at\n"
                    "  x = x₀ + v₀t + ½at²\n"
                    "  v² = v₀² + 2a(x - x₀)\n"
                    "  x = x₀ + ½(v + v₀)t\n\n"
                    "For projectile motion:\n"
                    "  Horizontal: a=0, x = v₀ₓ·t (constant velocity)\n"
                    "  Vertical:   a=-g = -9.81 m/s²\n\n"
                    "Angular kinematics (same form):\n"
                    "  ω = ω₀ + αt\n"
                    "  θ = θ₀ + ω₀t + ½αt²\n\n"
                    "Handbook: p.102 — Kinematics equations."
                ),
                "handbook_page": 102
            },
            {
                "title": "Work-Energy and Impulse-Momentum",
                "explanation": (
                    "Work-Energy Theorem:\n"
                    "  ΣW = ΔKE = ½mv₂² - ½mv₁²\n"
                    "  Gravity: W_gravity = mgh (+ when falling)\n"
                    "  Spring: W_spring = ½k(x₁² - x₂²)\n"
                    "  Friction: W_friction = -μ_k × N × d (always negative)\n\n"
                    "Impulse-Momentum:\n"
                    "  Impulse J = FΔt = Δ(mv) = m(v₂ - v₁)\n\n"
                    "Conservation of momentum (no external forces):\n"
                    "  m₁v₁ + m₂v₂ = m₁v₁' + m₂v₂'\n\n"
                    "Handbook: p.102 — Work, energy, impulse, momentum."
                ),
                "handbook_page": 102
            },
            {
                "title": "Vibrations — Natural Frequency and Damping",
                "explanation": (
                    "Spring-mass system:\n"
                    "  ωₙ = √(k/m)          [rad/s]\n"
                    "  fₙ = ωₙ/(2π)         [Hz]\n"
                    "  Tₙ = 1/fₙ = 2π/ωₙ   [s]\n\n"
                    "Damping:\n"
                    "  c_cr = 2√(km) = 2mωₙ  (critical damping coefficient)\n"
                    "  ζ = c/c_cr             (damping ratio)\n"
                    "  ζ < 1: underdamped — oscillatory\n"
                    "  ζ = 1: critically damped — fastest no-overshoot\n"
                    "  ζ > 1: overdamped — sluggish\n\n"
                    "Resonance: driving frequency = ωₙ → large amplitude\n\n"
                    "Handbook: p.102 — Vibrations."
                ),
                "handbook_page": 102
            }
        ]
    },
    {
        "id": 8,
        "name": "Mechanics of Materials",
        "q_range": "9–14",
        "handbook_page": 130,
        "baseline": "strong",
        "week": 4,
        "subtopics": ["Axial/Shear Stress", "Bending", "Torsion", "Mohr's Circle", "Column Buckling", "Thermal Stress"],
        "key_concepts": [
            {
                "title": "Core Stress Formulas — The Big Three",
                "explanation": (
                    "Axial:    σ = P/A\n"
                    "Bending:  σ = Mc/I   (c = distance from NA to outer fiber)\n"
                    "Torsion:  τ = Tc/J   (c = outer radius)\n\n"
                    "Section properties:\n"
                    "  Solid circle:  I = πd⁴/64    J = πd⁴/32\n"
                    "  Rectangle:     I = bh³/12\n\n"
                    "Shear formula: τ = VQ/(Ib)\n"
                    "  Q = first moment of area above the cut\n\n"
                    "Deformation:\n"
                    "  Axial: δ = PL/(AE)\n"
                    "  Torsion: φ = TL/(GJ)\n\n"
                    "Handbook: p.130 — Mechanics of materials formulas."
                ),
                "handbook_page": 130
            },
            {
                "title": "Mohr's Circle and Principal Stresses",
                "explanation": (
                    "Given: σₓ, σᵧ, τₓᵧ\n\n"
                    "Center:  σ_avg = (σₓ + σᵧ)/2\n"
                    "Radius:  R = √[((σₓ-σᵧ)/2)² + τₓᵧ²]\n\n"
                    "Principal stresses:\n"
                    "  σ₁ = σ_avg + R  (maximum)\n"
                    "  σ₂ = σ_avg - R  (minimum)\n\n"
                    "Max shear stress: τ_max = R\n\n"
                    "Principal angle: tan(2θₚ) = 2τₓᵧ/(σₓ - σᵧ)\n\n"
                    "Handbook: p.130 — Stress transformation, Mohr's circle."
                ),
                "handbook_page": 130
            },
            {
                "title": "Column Buckling and Beam Formulas",
                "explanation": (
                    "Euler buckling (critical load):\n"
                    "  P_cr = π²EI / (KL)²\n\n"
                    "Effective length factor K:\n"
                    "  Pin-pin: K = 1.0\n"
                    "  Fixed-free (flagpole): K = 2.0\n"
                    "  Fixed-pin: K = 0.7\n"
                    "  Fixed-fixed: K = 0.5\n\n"
                    "Slenderness ratio: KL/r  (r = √(I/A), radius of gyration)\n\n"
                    "Beam deflections — look up in handbook table (p.130):\n"
                    "  Simply supported, center load: δ_max = PL³/(48EI)\n"
                    "  Cantilever, end load: δ_max = PL³/(3EI)\n\n"
                    "Handbook: p.130 — Column buckling, beam deflection formulas."
                ),
                "handbook_page": 130
            }
        ]
    },
    {
        "id": 9,
        "name": "Material Properties and Processing",
        "q_range": "7–11",
        "handbook_page": 117,
        "baseline": "moderate",
        "week": 8,
        "subtopics": ["Stress-Strain", "Ferrous Metals", "Phase Diagrams", "Fatigue", "Corrosion", "Composites"],
        "key_concepts": [
            {
                "title": "Stress-Strain Diagram Features",
                "explanation": (
                    "Key points on a stress-strain diagram:\n\n"
                    "  Slope of elastic region: E (Young's modulus)\n"
                    "  Proportional limit: end of Hooke's law region\n"
                    "  Yield strength Sy: onset of plastic deformation\n"
                    "    (0.2% offset method for non-obvious yield)\n"
                    "  Ultimate tensile strength Su: maximum stress\n"
                    "  Fracture point: final failure\n\n"
                    "Ductile: large plastic region (steel, aluminum)\n"
                    "Brittle: fracture near yield, no plastic region (cast iron, ceramics)\n\n"
                    "Toughness = area under stress-strain curve (energy to fracture)\n\n"
                    "Handbook: p.117 — Mechanical properties, stress-strain."
                ),
                "handbook_page": 117
            },
            {
                "title": "Iron-Carbon Phase Diagram",
                "explanation": (
                    "Key compositions and temperatures:\n\n"
                    "  Eutectoid: 0.76% C, 727°C → pearlite on slow cooling\n"
                    "  Eutectic:  4.3% C, 1147°C → ledeburite\n\n"
                    "Phases:\n"
                    "  Ferrite (α): < 0.02% C, soft, BCC\n"
                    "  Austenite (γ): FCC, forms above 727°C\n"
                    "  Cementite (Fe₃C): 6.67% C, very hard and brittle\n"
                    "  Pearlite: lamellar α + Fe₃C (eutectoid mixture)\n"
                    "  Martensite: formed by quenching austenite — hard, brittle, BCT\n\n"
                    "Heat treatment: quench → martensite; temper → toughens martensite\n\n"
                    "Handbook: p.117 — Iron-carbon phase diagram."
                ),
                "handbook_page": 117
            },
            {
                "title": "Fatigue and Endurance Limit",
                "explanation": (
                    "Fatigue: failure under repeated/cyclic loading at σ < Sy\n\n"
                    "S-N curve (Wöhler curve): stress amplitude vs. cycles to failure\n"
                    "  Steel: endurance limit Se ≈ 0.5 × Sut (infinite life below Se)\n"
                    "  Aluminum: no true endurance limit (fatigue life at 10⁸ cycles)\n\n"
                    "Stress ratio: R = σ_min/σ_max\n"
                    "  R = -1: fully reversed (most damaging)\n"
                    "  R = 0: pulsating from zero\n\n"
                    "Goodman criterion (on FE exam):\n"
                    "  σ_a/Se + σ_m/Sut = 1 (failure line)\n"
                    "  Below line = safe\n\n"
                    "Handbook: p.117 — Fatigue, endurance limit."
                ),
                "handbook_page": 117
            }
        ]
    },
    {
        "id": 10,
        "name": "Fluid Mechanics",
        "q_range": "10–15",
        "handbook_page": 181,
        "baseline": "weak",
        "week": 5,
        "subtopics": ["Fluid Properties", "Fluid Statics", "Bernoulli", "Internal Flow", "Pump Laws", "Compressible Flow"],
        "key_concepts": [
            {
                "title": "Fluid Properties and Hydrostatics",
                "explanation": (
                    "Density: ρ_water = 1000 kg/m³ (1 g/cm³)\n"
                    "Specific gravity: SG = ρ_fluid/ρ_water\n"
                    "Dynamic viscosity: μ [Pa·s = kg/(m·s)]\n"
                    "Kinematic viscosity: ν = μ/ρ [m²/s]\n\n"
                    "Hydrostatic pressure: P = ρgh\n"
                    "  (gauge pressure — above atmospheric)\n"
                    "Absolute pressure = gauge + atmospheric (101.325 kPa)\n\n"
                    "Hydrostatic force on submerged surface:\n"
                    "  F = P_centroid × A\n"
                    "  Acts at the center of pressure (below centroid)\n\n"
                    "Handbook: p.181 — Fluid statics, fluid properties."
                ),
                "handbook_page": 181
            },
            {
                "title": "Bernoulli and Continuity",
                "explanation": (
                    "Continuity (incompressible): A₁v₁ = A₂v₂\n\n"
                    "Bernoulli (steady, inviscid, along streamline):\n"
                    "  P₁ + ½ρv₁² + ρgz₁ = P₂ + ½ρv₂² + ρgz₂\n"
                    "  Or in head form: P/γ + v²/2g + z = constant\n\n"
                    "When Bernoulli does NOT apply:\n"
                    "  • Viscous losses present (use energy equation with h_L)\n"
                    "  • Unsteady flow\n"
                    "  • Compressible flow (high Mach)\n"
                    "  • Across a pump or turbine\n\n"
                    "Energy equation with pump/head loss:\n"
                    "  P₁/γ + v₁²/2g + z₁ + h_p = P₂/γ + v₂²/2g + z₂ + h_L\n\n"
                    "Handbook: p.181 — Bernoulli, energy equation."
                ),
                "handbook_page": 181
            },
            {
                "title": "Pipe Flow, Reynolds Number, and Pump Laws",
                "explanation": (
                    "Reynolds number: Re = ρvD/μ = vD/ν\n"
                    "  Re < 2300: laminar flow\n"
                    "  Re > 4000: turbulent flow\n"
                    "  2300–4000: transitional\n\n"
                    "Darcy-Weisbach head loss:\n"
                    "  h_f = f × (L/D) × (v²/2g)\n"
                    "  f: friction factor — look up on Moody diagram (handbook p.181)\n\n"
                    "Pump affinity laws:\n"
                    "  Q ∝ N      (flow rate ∝ speed)\n"
                    "  H ∝ N²     (head ∝ speed squared)\n"
                    "  P ∝ N³     (power ∝ speed cubed)\n\n"
                    "Mach number: M = v/c (c = speed of sound ≈ 340 m/s in air)\n\n"
                    "Handbook: p.181 — Moody diagram, Darcy-Weisbach, pump laws."
                ),
                "handbook_page": 181
            }
        ]
    },
    {
        "id": 11,
        "name": "Thermodynamics",
        "q_range": "10–15",
        "handbook_page": 143,
        "baseline": "strong",
        "week": 6,
        "subtopics": ["Ideal Gas", "First/Second Law", "Power Cycles", "Refrigeration", "Psychrometrics"],
        "key_concepts": [
            {
                "title": "Ideal Gas Law and First Law",
                "explanation": (
                    "Ideal gas law: PV = nRT = mRT  (R_air = 0.287 kJ/kg·K)\n"
                    "  T must be in KELVIN (T[K] = T[°C] + 273.15)\n\n"
                    "First Law for closed system:\n"
                    "  Q - W = ΔU = m·cv·ΔT\n\n"
                    "Process types:\n"
                    "  Isothermal (T=const): PV = const, W = nRT·ln(V₂/V₁)\n"
                    "  Isobaric (P=const):   W = PΔV\n"
                    "  Isochoric (V=const):  W = 0, Q = ΔU\n"
                    "  Adiabatic (Q=0):      W = -ΔU, PV^k = const\n\n"
                    "Handbook: p.143 — Ideal gas, first law, processes."
                ),
                "handbook_page": 143
            },
            {
                "title": "Power Cycles and Efficiency",
                "explanation": (
                    "Carnot efficiency (maximum possible):\n"
                    "  η_Carnot = 1 - T_L/T_H  (temperatures in Kelvin!)\n\n"
                    "Rankine cycle (steam power plant):\n"
                    "  η = (W_turbine - W_pump) / Q_boiler\n"
                    "  W_turbine = h₃ - h₄  (look up steam tables)\n\n"
                    "Brayton cycle (gas turbine):\n"
                    "  η = 1 - 1/r_p^((k-1)/k)  where r_p = pressure ratio\n\n"
                    "Otto cycle (gasoline engine):\n"
                    "  η = 1 - 1/r_c^(k-1)  where r_c = compression ratio\n\n"
                    "COP — Refrigerator: COP_R = Q_L/W\n"
                    "COP — Heat pump:   COP_HP = Q_H/W = COP_R + 1\n\n"
                    "Handbook: p.143 — Power cycles, COP."
                ),
                "handbook_page": 143
            },
            {
                "title": "Steam Tables and Psychrometrics",
                "explanation": (
                    "Steam table navigation (handbook p.143):\n"
                    "  Saturated: given T or P → find h_f, h_fg, h_g, s_f, s_fg, s_g\n"
                    "  Superheated: given T and P → find h, s, v\n"
                    "  Quality: x = (h - h_f)/h_fg  (must be 0 ≤ x ≤ 1)\n\n"
                    "Two-phase mixture:\n"
                    "  h = h_f + x·h_fg\n"
                    "  s = s_f + x·s_fg\n\n"
                    "Psychrometrics:\n"
                    "  Relative humidity: φ = P_v/P_sat × 100%\n"
                    "  Humidity ratio: ω = 0.622 × P_v/(P - P_v)\n"
                    "  Dew point: temperature where φ = 100%\n\n"
                    "Handbook: p.143 — Steam tables, psychrometric chart."
                ),
                "handbook_page": 143
            }
        ]
    },
    {
        "id": 12,
        "name": "Heat Transfer",
        "q_range": "7–11",
        "handbook_page": 209,
        "baseline": "moderate",
        "week": 7,
        "subtopics": ["Conduction", "Convection", "Radiation", "Heat Exchangers", "Transient"],
        "key_concepts": [
            {
                "title": "Conduction — Fourier's Law and Thermal Resistance",
                "explanation": (
                    "Fourier's Law:\n"
                    "  q'' = -k dT/dx   [W/m²]\n"
                    "  Q = kA(ΔT)/L     [W]  (for flat wall)\n\n"
                    "Thermal resistance (analogy to Ohm's law):\n"
                    "  R_wall = L/(kA)      [K/W]\n"
                    "  R_conv = 1/(hA)\n"
                    "  R_cyl  = ln(r₂/r₁)/(2πkL)\n\n"
                    "Series resistances: R_total = ΣRᵢ\n"
                    "  Q = ΔT_total / R_total\n\n"
                    "Handbook: p.209 — Conduction, thermal resistance."
                ),
                "handbook_page": 209
            },
            {
                "title": "Convection and Radiation",
                "explanation": (
                    "Newton's law of cooling:\n"
                    "  Q = hA(T_surface - T_fluid)\n"
                    "  h: convection coefficient [W/m²·K]\n\n"
                    "Nusselt number: Nu = hL/k\n"
                    "  Higher Nu = more effective convection\n"
                    "  Nu correlations in handbook for forced convection\n\n"
                    "Stefan-Boltzmann radiation:\n"
                    "  q'' = εσT⁴  (blackbody: ε=1)\n"
                    "  σ = 5.67×10⁻⁸ W/m²·K⁴\n"
                    "  T must be in KELVIN\n\n"
                    "Net radiation between surfaces:\n"
                    "  Q = εσA(T₁⁴ - T₂⁴) × F₁₂ (view factor)\n\n"
                    "Handbook: p.209 — Convection correlations, radiation."
                ),
                "handbook_page": 209
            },
            {
                "title": "Heat Exchangers and Transient Analysis",
                "explanation": (
                    "LMTD Method:\n"
                    "  Q = UA × LMTD\n"
                    "  LMTD = (ΔT₁ - ΔT₂)/ln(ΔT₁/ΔT₂)\n"
                    "  For counterflow: ΔT₁=T_h,in-T_c,out  ΔT₂=T_h,out-T_c,in\n"
                    "  For parallel flow: ΔT₁=T_h,in-T_c,in  ΔT₂=T_h,out-T_c,out\n\n"
                    "Transient — Lumped Capacitance:\n"
                    "  Valid when Bi = hL_c/k < 0.1\n"
                    "  L_c = V/A_s (characteristic length)\n"
                    "  [T(t)-T_∞]/[T_i-T_∞] = exp(-t/τ_t)\n"
                    "  Time constant: τ_t = ρcV/(hA_s)\n\n"
                    "Handbook: p.209 — LMTD, Biot number, transient."
                ),
                "handbook_page": 209
            }
        ]
    },
    {
        "id": 13,
        "name": "Measurements, Instrumentation, and Controls",
        "q_range": "5–8",
        "handbook_page": 225,
        "baseline": "moderate",
        "week": 7,
        "subtopics": ["Sensors", "Control Systems", "Dynamic Response", "Measurement Uncertainty"],
        "key_concepts": [
            {
                "title": "PID Control",
                "explanation": (
                    "PID controller output: u(t) = K_p·e + K_i·∫e·dt + K_d·(de/dt)\n\n"
                    "Controller actions:\n"
                    "  P (Proportional): responds to current error — reduces error\n"
                    "    but may leave steady-state offset\n"
                    "  I (Integral): responds to accumulated error — eliminates\n"
                    "    steady-state error\n"
                    "  D (Derivative): responds to rate of error change — reduces\n"
                    "    overshoot, improves stability\n\n"
                    "P-only: offset remains     I eliminates offset\n"
                    "D dampens oscillations — think 'shock absorber'\n\n"
                    "Handbook: p.225 — Control systems, PID."
                ),
                "handbook_page": 225
            },
            {
                "title": "Block Diagrams and Transfer Functions",
                "explanation": (
                    "Transfer function: G(s) = Output(s)/Input(s)\n\n"
                    "Block diagram algebra:\n"
                    "  Series: G_total = G₁(s) × G₂(s)\n"
                    "  Parallel: G_total = G₁(s) + G₂(s)\n\n"
                    "Closed-loop system (negative feedback):\n"
                    "  T(s) = G(s) / [1 + G(s)H(s)]\n"
                    "  With unity feedback (H=1): T = G/(1+G)\n\n"
                    "Stability: system is stable if all poles have negative real parts.\n\n"
                    "First-order step response:\n"
                    "  y(t) = 1 - e^(-t/τ)  (reaches 63.2% at t=τ)\n\n"
                    "Handbook: p.225 — Block diagrams, transfer functions."
                ),
                "handbook_page": 225
            },
            {
                "title": "Measurement Error and Uncertainty",
                "explanation": (
                    "Accuracy: how close to the true value\n"
                    "Precision: how repeatable (consistent with each other)\n\n"
                    "Systematic error (bias): constant offset from true value\n"
                    "Random error: statistical scatter in readings\n\n"
                    "Error propagation:\n"
                    "  y = A + B: δy = √(δA² + δB²)\n"
                    "  y = A × B: δy/y = √((δA/A)² + (δB/B)²)\n\n"
                    "Significant figures:\n"
                    "  Result limited by measurement with fewest sig figs\n"
                    "  Trailing zeros after decimal point ARE significant\n\n"
                    "Handbook: p.225 — Measurement, error propagation."
                ),
                "handbook_page": 225
            }
        ]
    },
    {
        "id": 14,
        "name": "Mechanical Design and Analysis",
        "q_range": "10–15",
        "handbook_page": 436,
        "baseline": "strong",
        "week": 9,
        "subtopics": ["Failure Theories", "Springs", "Pressure Vessels", "Power Transmission", "GD&T"],
        "key_concepts": [
            {
                "title": "Failure Theories — Von Mises and Tresca",
                "explanation": (
                    "Von Mises (distortion energy theory) — most accurate for ductile:\n"
                    "  σ_e = √(σₓ² - σₓσᵧ + σᵧ² + 3τₓᵧ²)\n"
                    "  Simplified for uniaxial + shear: σ_e = √(σ² + 3τ²)\n"
                    "  Yield when: σ_e ≥ Sy\n\n"
                    "Tresca (max shear stress theory) — conservative:\n"
                    "  τ_max = (σ₁ - σ₂)/2\n"
                    "  Yield when: τ_max ≥ Sy/2\n\n"
                    "Goodman (fatigue — mean + alternating stress):\n"
                    "  σ_a/Se + σ_m/Sut = 1 (failure line)\n"
                    "  Design: σ_a/Se + σ_m/Sut < 1 (safe)\n\n"
                    "Handbook: p.436 — Failure theories."
                ),
                "handbook_page": 436
            },
            {
                "title": "Springs, Pressure Vessels, and Gears",
                "explanation": (
                    "Springs:\n"
                    "  Series: 1/k_eq = 1/k₁ + 1/k₂  (softer)\n"
                    "  Parallel: k_eq = k₁ + k₂       (stiffer)\n"
                    "  Coil spring: k = Gd⁴/(8ND³)\n\n"
                    "Thin-walled pressure vessel (t < r/10):\n"
                    "  Hoop (circumferential): σ_h = pr/t   ← largest stress\n"
                    "  Longitudinal:           σ_L = pr/2t  (half of hoop)\n\n"
                    "Gears:\n"
                    "  Gear ratio: N = N_teeth,out/N_teeth,in\n"
                    "  T_out = T_in × N  (torque multiplied)\n"
                    "  ω_out = ω_in / N  (speed divided)\n\n"
                    "Handbook: p.436 — Springs, pressure vessels, gears."
                ),
                "handbook_page": 436
            },
            {
                "title": "GD&T — Geometric Dimensioning and Tolerancing",
                "explanation": (
                    "Form controls (no datum needed):\n"
                    "  ─  Straightness: line element is straight\n"
                    "  ▱  Flatness: surface is flat\n"
                    "  ○  Circularity (roundness): each circular cross-section\n"
                    "  ⌭  Cylindricity: combines roundness + straightness\n\n"
                    "Orientation controls (datum required):\n"
                    "  //  Parallelism\n"
                    "  ⊥  Perpendicularity\n"
                    "  ∠  Angularity\n\n"
                    "Location controls:\n"
                    "  ⊕  True Position (most common in manufacturing)\n"
                    "  ◎  Concentricity\n\n"
                    "MMC = Maximum Material Condition (most material present)\n"
                    "LMC = Least Material Condition\n\n"
                    "Handbook: p.436 — GD&T symbols and definitions."
                ),
                "handbook_page": 436
            }
        ]
    }
]

# ─────────────────────────── Handbook Navigator ───────────────────────────────
HANDBOOK_MAP = {
    "units": (1, "Unit conversion tables — bookmark this page"),
    "conversion": (1, "Unit conversion tables — bookmark this page"),
    "ethics": (4, "NCEES Model Law and Model Rules — public welfare hierarchy"),
    "model law": (4, "NCEES Model Law and Model Rules"),
    "intellectual property": (4, "Patents, trade secrets, copyrights, trademarks"),
    "patent": (4, "Intellectual property — patents"),
    "copyright": (4, "Intellectual property — copyrights"),
    "math": (36, "Derivatives, integrals, ODEs, Laplace, matrices, numerical methods"),
    "mathematics": (36, "Derivatives, integrals, ODEs, Laplace, matrices, numerical methods"),
    "derivative": (36, "Calculus — differentiation rules"),
    "integral": (36, "Calculus — integration rules"),
    "laplace": (36, "Laplace transform pairs and properties"),
    "ode": (36, "Differential equations — first and second order"),
    "differential equation": (36, "ODEs — homogeneous and particular solutions"),
    "matrix": (36, "Linear algebra — matrix operations, determinant, inverse"),
    "newton method": (36, "Numerical methods — Newton-Raphson root finding"),
    "taylor": (36, "Taylor series expansion"),
    "statistics": (64, "Probability distributions, mean, std dev, regression, confidence intervals"),
    "probability": (64, "Probability — binomial, normal, expected value"),
    "normal distribution": (64, "Normal distribution — z-table, z = (x-μ)/σ"),
    "standard deviation": (64, "Sample and population standard deviation formulas"),
    "regression": (64, "Linear regression — slope, intercept, correlation r"),
    "confidence interval": (64, "Confidence intervals — z and t distributions"),
    "statics": (95, "FBD, equilibrium, trusses, centroids, moment of inertia, friction"),
    "centroid": (95, "Centroid table — rectangle, triangle, circle, semicircle"),
    "moment of inertia": (95, "Area moment of inertia table — standard shapes"),
    "truss": (95, "Truss — method of joints and sections"),
    "equilibrium": (95, "Equilibrium — ΣF=0, ΣM=0"),
    "friction": (95, "Static and kinetic friction — F = μN"),
    "dynamics": (102, "Kinematics equations, work-energy, impulse-momentum, vibrations"),
    "kinematics": (102, "Kinematics — v=v₀+at, x=x₀+v₀t+½at², projectile motion"),
    "work energy": (102, "Work-energy theorem — ΣW = ΔKE"),
    "impulse": (102, "Impulse-momentum — J = FΔt = mΔv"),
    "momentum": (102, "Linear and angular momentum"),
    "vibration": (102, "Natural frequency ωₙ=√(k/m), damping ratio ζ"),
    "natural frequency": (102, "ωₙ = √(k/m) — spring-mass natural frequency"),
    "damping": (102, "Damping ratio ζ = c/(2√(km)), underdamped/overdamped"),
    "materials": (117, "Stress-strain diagram, phase diagrams, fatigue, corrosion, composites"),
    "phase diagram": (117, "Iron-carbon phase diagram — eutectoid, eutectic, phases"),
    "fatigue": (117, "S-N curve, endurance limit Se ≈ 0.5 Sut, Goodman line"),
    "endurance limit": (117, "Se ≈ 0.5 × Sut for steel — infinite life below Se"),
    "corrosion": (117, "Galvanic corrosion, crevice, stress corrosion cracking"),
    "stress strain": (130, "Stress-strain formulas: σ=P/A, σ=Mc/I, τ=Tc/J"),
    "mechanics of materials": (130, "Axial, bending, torsion, shear, column buckling"),
    "bending": (130, "Flexure formula σ = Mc/I, beam deflection tables"),
    "torsion": (130, "Torsion τ = Tc/J, angle of twist φ = TL/(GJ)"),
    "mohr": (130, "Mohr's circle — principal stresses, max shear stress"),
    "principal stress": (130, "Principal stresses σ₁,σ₂ = σ_avg ± R"),
    "euler": (130, "Euler column buckling P_cr = π²EI/(KL)²"),
    "column": (130, "Column buckling — Euler formula, effective length K"),
    "beam deflection": (130, "Beam deflection formulas — cantilever, simply supported"),
    "thermodynamics": (143, "Ideal gas, first law, power cycles, refrigeration, steam tables, psychrometrics"),
    "steam table": (143, "Steam tables — saturated and superheated water/steam"),
    "rankine": (143, "Rankine cycle — steam power plant efficiency"),
    "brayton": (143, "Brayton cycle — gas turbine efficiency"),
    "carnot": (143, "Carnot efficiency η = 1 - T_L/T_H"),
    "refrigeration": (143, "COP_R = Q_L/W, COP_HP = Q_H/W = COP_R + 1"),
    "psychrometric": (143, "Psychrometric chart — humidity ratio, relative humidity, dew point"),
    "ideal gas": (143, "PV = nRT — ideal gas law"),
    "fluids": (181, "Bernoulli, continuity, Moody diagram, Darcy-Weisbach, pump laws"),
    "fluid mechanics": (181, "Bernoulli, continuity, Moody diagram, Darcy-Weisbach, pump laws"),
    "bernoulli": (181, "Bernoulli equation P + ½ρv² + ρgz = constant"),
    "reynolds": (181, "Reynolds number Re = ρvD/μ — laminar <2300, turbulent >4000"),
    "moody": (181, "Moody diagram — friction factor f vs Reynolds number and roughness"),
    "darcy": (181, "Darcy-Weisbach h_f = f(L/D)(v²/2g)"),
    "head loss": (181, "Head loss — Darcy-Weisbach equation, minor losses"),
    "pump": (181, "Pump affinity laws — Q∝N, H∝N², P∝N³"),
    "affinity": (181, "Pump/fan affinity laws — scaling laws"),
    "mach": (181, "Compressible flow — Mach number M = v/c, isentropic relations"),
    "compressible": (181, "Compressible flow — Mach, isentropic, normal shock"),
    "heat transfer": (209, "Conduction, convection, radiation, LMTD, heat exchangers, Biot number"),
    "fourier": (209, "Fourier's law q'' = -k(dT/dx) — conduction"),
    "conduction": (209, "Fourier's law, thermal resistance R = L/(kA)"),
    "convection": (209, "Newton's law Q = hA(T_s - T_∞), Nusselt number"),
    "nusselt": (209, "Nusselt number Nu = hL/k — convection correlation"),
    "stefan": (209, "Stefan-Boltzmann law E = εσT⁴, σ = 5.67×10⁻⁸ W/m²·K⁴"),
    "radiation": (209, "Radiation — Stefan-Boltzmann, view factors"),
    "lmtd": (209, "LMTD = (ΔT₁-ΔT₂)/ln(ΔT₁/ΔT₂) — heat exchanger"),
    "heat exchanger": (209, "LMTD method, effectiveness-NTU method"),
    "biot": (209, "Biot number Bi = hL/k — lumped capacitance valid if Bi < 0.1"),
    "transient": (209, "Transient conduction — Biot number, lumped capacitance, Heisler charts"),
    "controls": (225, "PID control, block diagrams, transfer functions, time constants"),
    "pid": (225, "PID controller — proportional, integral, derivative actions"),
    "transfer function": (225, "Transfer function G(s), closed-loop T = G/(1+GH)"),
    "block diagram": (225, "Block diagram algebra — series (×), parallel (+), feedback"),
    "time constant": (225, "First-order system — τ, reaches 63.2% at t = τ"),
    "economics": (235, "P/F, F/P, A/P, P/A interest factor tables, BCR, IRR"),
    "engineering economics": (235, "Interest factors, present worth, annual worth, BCR, IRR"),
    "interest factor": (235, "P/F, F/P, A/P, P/A, F/A — look up, never memorize"),
    "present worth": (235, "Present worth — P = F × (P/F, i%, n)"),
    "future worth": (235, "Future worth — F = P × (F/P, i%, n)"),
    "mechanical design": (436, "Failure theories, springs, pressure vessels, gears, GD&T"),
    "von mises": (436, "Von Mises σ_e = √(σ²+3τ²) — ductile failure criterion"),
    "goodman": (436, "Goodman σ_a/Se + σ_m/Sut = 1 — fatigue design criterion"),
    "spring": (436, "Springs: series 1/k=Σ(1/kᵢ), parallel k=Σkᵢ, coil k=Gd⁴/(8ND³)"),
    "pressure vessel": (436, "Thin-wall: σ_hoop = pr/t, σ_long = pr/2t"),
    "gear": (436, "Gear ratio N=teeth_out/teeth_in, T_out=T_in×N, ω_out=ω_in/N"),
    "gdt": (436, "GD&T symbols — flatness, straightness, true position, perpendicularity"),
    "geometric dimensioning": (436, "GD&T — form, orientation, and location tolerances"),
    "kirchhoff": (270, "KVL: sum of voltages in loop = 0; KCL: currents in = currents out"),
    "ohm": (270, "Ohm's law V = IR; Power P = IV = I²R = V²/R"),
    "phasor": (270, "AC circuits — phasor representation, impedance Z = R + jX"),
    "impedance": (270, "Impedance Z: Z_R=R, Z_L=jωL, Z_C=1/(jωC)"),
}

# ─────────────────────────── Exam Tips ────────────────────────────────────────
EXAM_TIPS = [
    "2-MINUTE RULE: If you're stuck after 90 seconds, flag and move on. Come back with fresh eyes.",
    "UNIT CHECK FIRST: 80% of wrong answers come from unit errors. Check units before calculating.",
    "HANDBOOK SPEED: Practice finding 20 random topics in under 15 seconds each. Speed = extra time.",
    "NEVER LEAVE A BLANK: No penalty for wrong answers. Guess on unknowns — you have a 25% floor.",
    "DIFFICULTY STRATEGY: Easy <90s → Medium 2-3 min → Hard: flag it and come back.",
    "SUNK COST TRAP: If a question mentions money already spent, ignore it. Only future costs matter.",
    "KELVIN ALWAYS: Any thermodynamics formula with T? Use Kelvin. T[K] = T[°C] + 273.15.",
    "PUBLIC WELFARE WINS: On every ethics question, the answer that protects public safety is correct.",
    "CALCULATOR FLUENCY: Use the TI-36X Pro matrix solver for simultaneous equations. Don't do it by hand.",
    "LOOK UP FACTORS: Never memorize P/F, A/P interest factors. Open the handbook table and look them up.",
    "FBD FIRST: In any statics or dynamics problem, draw the free body diagram before touching numbers.",
    "BIG FOUR: Dynamics (10-15Q) + Fluids (10-15Q) + Thermo (10-15Q) + Mech Design (10-15Q) = up to 55% of exam.",
    "TUTORIAL: Do the on-screen tutorial at the start of the exam — it shows how to navigate the digital handbook.",
    "BREAK STRATEGY: Use the optional 25-minute break between sessions. Eat something. Reset your mind.",
    "ARRIVE EARLY: 15-30 min early at Prometric. Bring valid ID, TI-36X Pro, and a layer — centers are cold.",
]

# ─────────────────────────── Utility Functions ────────────────────────────────
def clear():
    os.system('clear')

def divider(char="─"):
    print(char * WIDTH)

def wrap(text, indent=0):
    prefix = " " * indent
    for line in text.split('\n'):
        if line.strip() == "":
            print()
        else:
            print(textwrap.fill(line, width=WIDTH, initial_indent=prefix, subsequent_indent=prefix))

def banner(text):
    divider("═")
    print(f"  {text}")
    divider("═")

def header(text):
    divider()
    print(f"  {text}")
    divider()

def prompt(text):
    try:
        return input(f"\n{text} ").strip().upper()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting tutor. Good luck on the exam!")
        sys.exit(0)

def wait():
    try:
        input("\n  [Press ENTER to continue]")
    except (KeyboardInterrupt, EOFError):
        sys.exit(0)

# ─────────────────────────── Data Loading ─────────────────────────────────────
def load_config():
    defaults = {
        "study_start_date": str(STUDY_START),
        "exam_date": DEFAULT_EXAM_DATE,
        "weekly_hour_target": WEEKLY_HOUR_TARGET,
        "show_hard_problems": False
    }
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE) as f:
                cfg = json.load(f)
            defaults.update(cfg)
        except Exception:
            pass
    return defaults

def save_config(cfg):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(cfg, f, indent=2)

def load_progress():
    defaults = {
        "sessions": [],
        "seen_problem_ids": [],
        "topic_accuracy": {str(i): {"correct": 0, "total": 0} for i in range(1, 15)},
        "weekly_hours": {str(i): 0.0 for i in range(1, 12)},
        "exam_date": DEFAULT_EXAM_DATE,
        "wrong_problems": []
    }
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE) as f:
                saved = json.load(f)
            for key in defaults:
                if key in saved:
                    defaults[key] = saved[key]
        except Exception:
            pass
    return defaults

def save_progress(progress):
    with open(PROGRESS_FILE, 'w') as f:
        json.dump(progress, f, indent=2)

def load_problems():
    try:
        with open(PROBLEMS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"\n  ERROR: problems.json not found at {PROBLEMS_FILE}")
        print("  Make sure problems.json is in the same directory as fe_tutor.py")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"\n  ERROR: Invalid JSON in problems.json: {e}")
        sys.exit(1)

# ─────────────────────────── Week Calculation ─────────────────────────────────
def get_current_week(cfg):
    start = datetime.date.fromisoformat(cfg["study_start_date"])
    today = datetime.date.today()
    delta = (today - start).days
    if delta < 0:
        return 0
    week = delta // 7 + 1
    return min(week, 11)

def get_week_dates(week, cfg):
    start = datetime.date.fromisoformat(cfg["study_start_date"])
    week_start = start + datetime.timedelta(days=(week - 1) * 7)
    week_end = week_start + datetime.timedelta(days=6)
    return week_start, week_end

def get_days_to_exam(cfg):
    exam = datetime.date.fromisoformat(cfg["exam_date"])
    today = datetime.date.today()
    return max(0, (exam - today).days)

# ─────────────────────────── Dashboard ───────────────────────────────────────
def show_dashboard(cfg, progress):
    clear()
    banner("FE MECHANICAL EXAM TUTOR  ⚙  NCEES FE Mechanical")

    week = get_current_week(cfg)
    days_left = get_days_to_exam(cfg)
    exam_date = cfg["exam_date"]

    # Current week topics
    week_topic_names = []
    for t in TOPICS:
        if t["week"] == week:
            week_topic_names.append(t["name"])

    ws, we = get_week_dates(week, cfg)
    print(f"\n  📅  Week {week} of 11  ·  {ws.strftime('%b %-d')} – {we.strftime('%b %-d, %Y')}")
    print(f"  🎯  Exam: {exam_date}  ·  {days_left} days away")
    if week_topic_names:
        print(f"  📚  This week: {', '.join(week_topic_names)}")
    else:
        print(f"  📚  This week: Review / Practice Exam")

    # Weekly hours
    hours_this_week = progress["weekly_hours"].get(str(week), 0.0)
    target = cfg.get("weekly_hour_target", 13)
    pct = min(1.0, hours_this_week / target)
    bar_filled = int(pct * 20)
    bar = "█" * bar_filled + "░" * (20 - bar_filled)
    print(f"\n  Hours this week: [{bar}] {hours_this_week:.1f}/{target}h")

    # Topic readiness
    print()
    divider()
    print("  TOPIC READINESS")
    divider()

    baseline_map = {"strong": "✅ Strong  ", "moderate": "🟡 Moderate", "weak": "🔴 Weak   "}

    for t in TOPICS:
        acc = progress["topic_accuracy"].get(str(t["id"]), {"correct": 0, "total": 0})
        total = acc["total"]
        star = "▶ " if t["week"] == week else "  "

        if total >= 3:
            pct_correct = acc["correct"] / total
            if pct_correct >= 0.75:
                status = "✅ " + f"{pct_correct*100:.0f}%"
            elif pct_correct >= 0.55:
                status = "🟡 " + f"{pct_correct*100:.0f}%"
            else:
                status = "🔴 " + f"{pct_correct*100:.0f}%"
        else:
            status = baseline_map.get(t["baseline"], "❓ Unknown ")

        q_info = f"({t['q_range']} Qs)"
        name_padded = t["name"][:32].ljust(33)
        print(f"  {star}[{t['id']:2d}] {name_padded} {status}  {q_info}")

    print()

# ─────────────────────────── Topic Menu ──────────────────────────────────────
def topic_menu(cfg, progress, problems):
    while True:
        show_dashboard(cfg, progress)
        print()
        print("  MENU:")
        print("   [1-14] Select topic")
        print("   [t]    This week's topic")
        print("   [h]    Handbook navigator (Find it fast)")
        print("   [r]    Review wrong problems")
        print("   [s]    Settings")
        print("   [q]    Quit")

        choice = prompt("Choice:")

        if choice == "Q":
            return
        elif choice == "T":
            week = get_current_week(cfg)
            week_topics = [t for t in TOPICS if t["week"] == week]
            if week_topics:
                topic_submenu(week_topics[0], cfg, progress, problems)
            else:
                print("\n  No specific topic for this week — try full practice mode!")
                wait()
        elif choice == "H":
            handbook_navigator()
        elif choice == "R":
            review_wrong_problems(progress, problems)
        elif choice == "S":
            settings_menu(cfg, progress)
        else:
            try:
                tid = int(choice)
                if 1 <= tid <= 14:
                    topic = next((t for t in TOPICS if t["id"] == tid), None)
                    if topic:
                        topic_submenu(topic, cfg, progress, problems)
                else:
                    print("\n  Invalid choice. Enter 1-14, t, h, r, s, or q.")
                    time.sleep(1)
            except ValueError:
                print("\n  Invalid choice. Enter 1-14, t, h, r, s, or q.")
                time.sleep(1)

# ─────────────────────────── Topic Submenu ───────────────────────────────────
def topic_submenu(topic, cfg, progress, problems):
    while True:
        clear()
        header(f"TOPIC {topic['id']}: {topic['name'].upper()}")
        print(f"\n  Handbook: p.{topic['handbook_page']}")
        print(f"  Exam questions: {topic['q_range']}")
        print(f"  Your status: {topic['baseline'].upper()}")
        print(f"\n  Subtopics covered:")
        for s in topic["subtopics"]:
            print(f"    • {s}")

        acc = progress["topic_accuracy"].get(str(topic["id"]), {"correct": 0, "total": 0})
        if acc["total"] > 0:
            pct = acc["correct"] / acc["total"] * 100
            print(f"\n  Your accuracy: {acc['correct']}/{acc['total']} = {pct:.0f}%")

        print("\n  [s] Study mode   [q] Quiz mode   [b] Back")
        choice = prompt("Choice:")

        if choice == "B":
            return
        elif choice == "S":
            study_mode(topic)
        elif choice == "Q":
            quiz_mode(topic, cfg, progress, problems)
        else:
            print("  Invalid. Enter s, q, or b.")
            time.sleep(1)

# ─────────────────────────── Study Mode ──────────────────────────────────────
def study_mode(topic):
    clear()
    banner(f"STUDY MODE: {topic['name'].upper()}")
    print(f"\n  Handbook reference: p.{topic['handbook_page']}")
    print(f"  Expected questions on exam: {topic['q_range']}")
    print()

    concepts = topic.get("key_concepts", [])
    if not concepts:
        print("  No study content available for this topic yet.")
        wait()
        return

    i = 0
    while i < len(concepts):
        concept = concepts[i]
        clear()
        header(f"Concept {i+1}/{len(concepts)}: {concept['title']}")
        print(f"  Handbook: p.{concept['handbook_page']}\n")
        wrap(concept["explanation"], indent=2)

        print(f"\n  [g] Got it — next concept")
        print(f"  [q] Quiz me on this topic now")
        print(f"  [p] Previous concept")
        print(f"  [b] Back to topic menu")
        choice = prompt("Choice:").upper()

        if choice == "G" or choice == "N":
            i += 1
        elif choice == "Q":
            return "quiz"
        elif choice == "P":
            i = max(0, i - 1)
        elif choice == "B":
            return
        else:
            i += 1

    clear()
    print(f"\n  ✅  You've reviewed all {len(concepts)} concepts for {topic['name']}!")
    print(f"\n  Now test yourself: run Quiz mode to check your understanding.")
    wait()

# ─────────────────────────── Quiz Mode ───────────────────────────────────────
def quiz_mode(topic, cfg, progress, problems, subtopic=None):
    show_hard = cfg.get("show_hard_problems", False)

    # Filter problems
    pool = [p for p in problems if p["topic_id"] == topic["id"]]
    if subtopic:
        pool = [p for p in pool if subtopic.lower() in p["subtopic"].lower()]
    if not show_hard:
        pool = [p for p in pool if p["difficulty"] != "hard"]

    seen = set(progress.get("seen_problem_ids", []))
    unseen = [p for p in pool if p["id"] not in seen]
    if not unseen:
        # Reset seen for this topic if all exhausted
        seen_this_topic = {p["id"] for p in pool}
        progress["seen_problem_ids"] = [x for x in progress["seen_problem_ids"] if x not in seen_this_topic]
        unseen = pool[:]

    random.shuffle(unseen)

    session_correct = 0
    session_total = 0
    session_times = []
    session_start = time.time()

    clear()
    banner(f"QUIZ: {topic['name'].upper()}")
    print(f"  {len(unseen)} problems available")
    print(f"  Target: < 2 minutes per problem")
    print(f"  Difficulty: {'Easy + Medium + Hard' if show_hard else 'Easy + Medium only'}")
    print(f"\n  TIP: Answer A, B, C, or D. [s] to skip, [b] to finish session.")
    wait()

    for problem in unseen:
        clear()
        header(f"QUIZ — {topic['name'].upper()}")

        diff_icon = {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}.get(problem["difficulty"], "")
        print(f"  Problem {session_total+1}  ·  {diff_icon}  ·  {problem['subtopic']}")
        divider()
        print()
        wrap(problem["question"], indent=2)
        print()
        for letter in ["A", "B", "C", "D"]:
            val = problem["choices"].get(letter, "")
            print(f"    {letter}) {val}")

        print(f"\n  ⏱  Timer running... (target: 2 min)")
        t_start = time.time()

        answer = prompt("Answer (A/B/C/D) or [s]kip, [b] back:").upper()

        t_elapsed = time.time() - t_start

        if answer == "B":
            break
        if answer == "S":
            print("\n  Skipped.")
            time.sleep(1)
            continue

        # Mark as seen
        if problem["id"] not in progress["seen_problem_ids"]:
            progress["seen_problem_ids"].append(problem["id"])

        correct_answer = problem["answer"]
        is_correct = (answer == correct_answer)
        session_total += 1
        session_times.append(t_elapsed)

        # Update accuracy
        acc = progress["topic_accuracy"].setdefault(str(topic["id"]), {"correct": 0, "total": 0})
        acc["total"] += 1
        if is_correct:
            acc["correct"] += 1
            session_correct += 1
        else:
            wrong_entry = {
                "problem_id": problem["id"],
                "topic_id": topic["id"],
                "topic_name": topic["name"],
                "question": problem["question"][:80],
                "your_answer": answer,
                "correct_answer": correct_answer
            }
            if not any(w["problem_id"] == problem["id"] for w in progress["wrong_problems"]):
                progress["wrong_problems"].append(wrong_entry)

        # Show result
        clear()
        if is_correct:
            print(f"\n  ✅  CORRECT!\n")
        else:
            print(f"\n  ❌  INCORRECT. The correct answer is: {correct_answer}\n")

        if t_elapsed > 120:
            print(f"  ⚠  Over 2-minute target (took {t_elapsed:.1f}s — flag these on exam day)")
        else:
            print(f"  ⏱  Time: {t_elapsed:.1f}s")

        print()
        divider()
        print("  SOLUTION:")
        divider()
        print()
        wrap(problem["solution"], indent=2)
        print(f"\n  📖  Handbook reference: p.{problem['handbook_page']}")

        print(f"\n  [n] Next problem   [b] End session")
        choice = prompt("Choice:").upper()
        if choice == "B":
            break

    # Session summary
    clear()
    banner("SESSION COMPLETE")
    print(f"\n  Topic: {topic['name']}")
    print(f"  Score: {session_correct}/{session_total} correct", end="")
    if session_total > 0:
        print(f"  ({session_correct/session_total*100:.0f}%)")
    else:
        print()

    if session_times:
        avg_time = sum(session_times) / len(session_times)
        over_time = sum(1 for t in session_times if t > 120)
        print(f"  Avg time: {avg_time:.1f}s per problem")
        if over_time:
            print(f"  ⚠  {over_time} problem(s) over 2-minute target")

    # Cumulative accuracy
    acc = progress["topic_accuracy"].get(str(topic["id"]), {"correct": 0, "total": 0})
    if acc["total"] > 0:
        print(f"\n  Cumulative accuracy for {topic['name']}: {acc['correct']}/{acc['total']} = {acc['correct']/acc['total']*100:.0f}%")

    if session_total > 0 and session_correct / session_total < 0.7:
        print(f"\n  ⚠  Below 70% — revisit Study mode for this topic before next quiz.")

    # Save session
    progress["sessions"].append({
        "date": str(datetime.date.today()),
        "topic_id": topic["id"],
        "topic_name": topic["name"],
        "correct": session_correct,
        "total": session_total
    })
    save_progress(progress)

    wait()

# ─────────────────────────── Handbook Navigator ──────────────────────────────
def handbook_navigator():
    while True:
        clear()
        banner("HANDBOOK NAVIGATOR  📖  Find It Fast")
        print("\n  Type a topic keyword to find its handbook page.")
        print("  Examples: bernoulli, euler, goodman, steam table, pid")
        print("  [b] to go back\n")
        divider()

        query = prompt("Search:").lower()

        if query == "B":
            return

        if not query:
            continue

        matches = {}
        for key, (page, desc) in HANDBOOK_MAP.items():
            if query in key or key in query:
                matches[key] = (page, desc)

        # Also do partial word matching
        query_words = query.split()
        for key, (page, desc) in HANDBOOK_MAP.items():
            key_words = key.split()
            if any(w in key for w in query_words):
                matches[key] = (page, desc)

        clear()
        banner("HANDBOOK NAVIGATOR  📖  Results")
        print(f"\n  Search: '{query}'\n")
        divider()

        if matches:
            # Sort by page number
            sorted_matches = sorted(set(matches.values()), key=lambda x: x[0])
            seen_pages = set()
            for page, desc in sorted_matches:
                if page not in seen_pages:
                    print(f"\n  📄  Page {page}")
                    wrap(desc, indent=6)
                    seen_pages.add(page)
        else:
            print(f"\n  No matches for '{query}'.")
            print("  Try: math, statics, fluids, thermodynamics, heat transfer,")
            print("       controls, economics, bernoulli, mohr, euler, goodman, pid")

        print(f"\n  [s] Search again   [b] Back to menu")
        choice = prompt("Choice:").upper()
        if choice == "B":
            return

# ─────────────────────────── Review Wrong Problems ───────────────────────────
def review_wrong_problems(progress, problems):
    wrong = progress.get("wrong_problems", [])
    if not wrong:
        clear()
        print("\n  No wrong problems on record yet. Go do some quizzes!")
        wait()
        return

    clear()
    banner("REVIEW — YOUR WRONG PROBLEMS")
    print(f"\n  {len(wrong)} problem(s) to review\n")
    divider()

    for i, entry in enumerate(wrong, 1):
        print(f"\n  [{i}] {entry['topic_name']}: {entry['question'][:60]}...")
        print(f"      Your answer: {entry['your_answer']}  |  Correct: {entry['correct_answer']}")

    print(f"\n  [c] Clear list   [b] Back")
    choice = prompt("Choice:").upper()
    if choice == "C":
        progress["wrong_problems"] = []
        save_progress(progress)
        print("\n  Wrong problem list cleared.")
        time.sleep(1)

# ─────────────────────────── Settings ────────────────────────────────────────
def settings_menu(cfg, progress):
    while True:
        clear()
        banner("SETTINGS")
        print(f"\n  [1] Exam date: {cfg['exam_date']}")
        print(f"  [2] Log study hours for current week")
        print(f"  [3] Toggle hard problems: {'ON' if cfg.get('show_hard_problems') else 'OFF'}")
        print(f"  [4] Reset all progress (WARNING: clears accuracy history)")
        print(f"  [b] Back")

        choice = prompt("Choice:")

        if choice == "B":
            return
        elif choice == "1":
            print(f"\n  Current exam date: {cfg['exam_date']}")
            new_date = prompt("Enter new exam date (YYYY-MM-DD) or [b] to cancel:").lower()
            if new_date != "B":
                try:
                    datetime.date.fromisoformat(new_date)
                    cfg["exam_date"] = new_date
                    save_config(cfg)
                    print(f"  Exam date set to {new_date}")
                    time.sleep(1.5)
                except ValueError:
                    print("  Invalid date format. Use YYYY-MM-DD.")
                    time.sleep(1.5)
        elif choice == "2":
            week = get_current_week(cfg)
            current = progress["weekly_hours"].get(str(week), 0.0)
            print(f"\n  Current hours logged for Week {week}: {current:.1f}h")
            hours_str = prompt("Hours to add (e.g. 1.5):").lower()
            if hours_str != "B":
                try:
                    hours = float(hours_str)
                    progress["weekly_hours"][str(week)] = current + hours
                    save_progress(progress)
                    print(f"  Logged! Week {week} total: {progress['weekly_hours'][str(week)]:.1f}h")
                    time.sleep(1.5)
                except ValueError:
                    print("  Invalid number.")
                    time.sleep(1.5)
        elif choice == "3":
            cfg["show_hard_problems"] = not cfg.get("show_hard_problems", False)
            save_config(cfg)
            state = "ON" if cfg["show_hard_problems"] else "OFF"
            print(f"  Hard problems: {state}")
            time.sleep(1)
        elif choice == "4":
            confirm = prompt("Type YES to confirm reset:").upper()
            if confirm == "YES":
                progress["topic_accuracy"] = {str(i): {"correct": 0, "total": 0} for i in range(1, 15)}
                progress["seen_problem_ids"] = []
                progress["wrong_problems"] = []
                progress["sessions"] = []
                save_progress(progress)
                print("  Progress reset.")
                time.sleep(1.5)

# ─────────────────────────── Exam Simulation ─────────────────────────────────
def exam_simulation(cfg, problems):
    clear()
    banner("EXAM SIMULATION MODE  ⏱  110 Questions / 5h 20min")
    print("\n  This simulates the real FE exam experience.")
    print("  • 110 questions served in random order")
    print("  • No feedback until the end")
    print("  • Timed: 320 minutes total (2.9 min/question average)")
    print("  • You can flag questions and return to them")
    print()
    print("  Are you sure you want to start? This cannot be paused.")
    confirm = prompt("Type START to begin, or [b] to cancel:").upper()
    if confirm != "START":
        return

    pool = problems[:]
    random.shuffle(pool)
    exam_pool = pool[:110]

    answers = {}
    flagged = set()
    start_time = time.time()
    total_time = 320 * 60  # seconds

    i = 0
    while i < len(exam_pool):
        elapsed = time.time() - start_time
        remaining = total_time - elapsed
        if remaining <= 0:
            print("\n  ⏰  TIME UP!")
            break

        mins_left = int(remaining // 60)
        secs_left = int(remaining % 60)

        problem = exam_pool[i]
        clear()
        flag_mark = " [FLAGGED]" if i in flagged else ""
        print(f"  Question {i+1}/110  ·  Time left: {mins_left}:{secs_left:02d}{flag_mark}")
        divider()
        print()
        wrap(problem["question"], indent=2)
        print()
        for letter in ["A", "B", "C", "D"]:
            val = problem["choices"].get(letter, "")
            marker = " ← your answer" if answers.get(i) == letter else ""
            print(f"    {letter}) {val}{marker}")

        print("\n  [A-D] Answer   [f] Flag/unflag   [p] Previous   [n] Next   [done] Finish")
        choice = prompt("Choice:").upper()

        if choice in ["A", "B", "C", "D"]:
            answers[i] = choice
            i += 1
        elif choice == "F":
            if i in flagged:
                flagged.discard(i)
            else:
                flagged.add(i)
        elif choice == "P":
            i = max(0, i - 1)
        elif choice == "N":
            i += 1
        elif choice == "DONE":
            break

    # Score
    clear()
    banner("EXAM SIMULATION — RESULTS")
    correct = 0
    topic_results = {}

    for idx, problem in enumerate(exam_pool[:i+1]):
        user_ans = answers.get(idx, "")
        if user_ans == problem["answer"]:
            correct += 1
        tid = str(problem["topic_id"])
        if tid not in topic_results:
            topic_results[tid] = {"correct": 0, "total": 0, "name": problem["topic_name"]}
        topic_results[tid]["total"] += 1
        if user_ans == problem["answer"]:
            topic_results[tid]["correct"] += 1

    answered = len(answers)
    total = len(exam_pool[:i+1])
    print(f"\n  Questions answered: {answered}/{total}")
    print(f"  Correct: {correct}/{answered} = {correct/answered*100:.1f}%" if answered else "")
    print()
    divider()
    print("  BREAKDOWN BY TOPIC")
    divider()
    for tid in sorted(topic_results.keys(), key=int):
        r = topic_results[tid]
        if r["total"] > 0:
            pct = r["correct"] / r["total"] * 100
            bar = "✅" if pct >= 70 else ("🟡" if pct >= 50 else "🔴")
            print(f"  {bar} {r['name'][:30]}: {r['correct']}/{r['total']} ({pct:.0f}%)")

    elapsed_min = int((time.time() - start_time) / 60)
    print(f"\n  Time used: {elapsed_min} minutes")
    if answered > 0 and correct / answered >= 0.70:
        print("\n  🎉  Passing-level score! Keep it up.")
    else:
        print("\n  📚  Below passing threshold. Review weak areas and re-test.")

    wait()

# ─────────────────────────── Main ─────────────────────────────────────────────
def main():
    cfg = load_config()

    # First run: set study start to today so Week 1 begins now
    if not os.path.exists(PROGRESS_FILE):
        cfg["study_start_date"] = str(datetime.date.today())
        save_config(cfg)

    progress = load_progress()
    problems = load_problems()

    week = get_current_week(cfg)

    # Offer exam simulation in week 10+
    while True:
        show_dashboard(cfg, progress)

        print()
        print("  MENU:")
        print("   [1-14] Select topic")
        print("   [t]    This week's topic  (Week %d: %s)" % (
            week,
            ", ".join(t["name"] for t in TOPICS if t["week"] == week) or "Practice Exam"
        ))
        print("   [h]    Handbook navigator (Find it fast)")
        print("   [r]    Review wrong problems")
        if week >= 10:
            print("   [e]    Exam simulation (110Q timed)")
        print("   [s]    Settings")
        print("   [q]    Quit")

        choice = prompt("Choice:")

        if choice == "Q":
            clear()
            tip = random.choice(EXAM_TIPS)
            print()
            divider("═")
            print("  EXAM TIP OF THE DAY:")
            divider()
            wrap(tip, indent=2)
            divider("═")
            print("\n  Study hard. You've got this.\n")
            break
        elif choice == "T":
            week_topics = [t for t in TOPICS if t["week"] == week]
            if week_topics:
                topic_submenu(week_topics[0], cfg, progress, problems)
            else:
                print("\n  Week 10-11: Use Exam Simulation mode [e] for practice exams!")
                time.sleep(2)
        elif choice == "H":
            handbook_navigator()
        elif choice == "R":
            review_wrong_problems(progress, problems)
        elif choice == "E" and week >= 10:
            exam_simulation(cfg, problems)
        elif choice == "S":
            settings_menu(cfg, progress)
        else:
            try:
                tid = int(choice)
                if 1 <= tid <= 14:
                    topic = next((t for t in TOPICS if t["id"] == tid), None)
                    if topic:
                        topic_submenu(topic, cfg, progress, problems)
                else:
                    print("\n  Invalid. Enter 1-14, t, h, r, s, or q.")
                    time.sleep(1)
            except ValueError:
                print("\n  Invalid. Enter 1-14, t, h, r, s, or q.")
                time.sleep(1)

if __name__ == "__main__":
    main()
