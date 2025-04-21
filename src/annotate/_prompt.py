ONTOLOGY = '''
# Property
* Self-Driven Entities
    * Living Beings
        * Human
        * Other Animals
        * Plants
    * Man-made Machines
        * Vehicles
        * Industrial Machines
* Externally Driven Entities
    * Solid
        * Rigid-body Solid
        * Deformable-body Solid
    * Liquid
    * Gas
# Dynamics
* Motion
    * Solid Motion
        * Linear Motion
        * Projectile Motion
        * Rotational Motion
        * Circular Motion
        * Oscillation
        * Complex Curvilinear Motion
        * Collision Dynamics
    * Biological and Biomechanical Motion
        * Human and Animal Motion
            * Walking, Running, and Jumping
            * Swimming
            * Flying
        * Organic Growth and Decomposition
            * Plant Growth
            * Decay and Decomposition
    * Liquid Motion
        * Pouring
        * Splashes and Waves
        * Dripping and Leaking
    * Airflow and Aerodynamics
        * Wind Effects
        * Smoke and Gas Dispersion
        * Vortex Formation
    * Buoyancy and Floating
        * Floating vs. Sinking
        * Submersion and Surfacing
* Deformations
    * Elastic and Plastic Deformations
        * Stretching and Compressing
        * Bending and Breaking
        * Soft Body Deformation
    * Fragmentation and Material Failure
        * Cracking and Shattering
        * Erosion and Wear
        * Disintegration
* Thermodynamics (Phase Transitions)
    * Solidification
    * Melting
    * Liquefaction
    * Boiling
    * Deposition
    * Sublimation
* Light Dynamics
    * Reflection
    * Refraction
    * Dispersion
    * Absorption
* Electromagnetic and Plasma Dynamics
    * Electromagnetic Forces
        * Magnetism
        * Static Electricity
    * Plasma and Ionized Gas Effects
        * Lightning and sparks
        * Plasma generation
* Chemical and Reactive Dynamics
    * Combustion and Explosions
        * Fire Spreading
        * Chemical Explosions
    * Chemical Reactions and Mixing
        * Dissolution and Diffusion
        * Corrosion and Oxidation
* Geological and Environmental Dynamics
    * Earth Surface Changes
        * Landslides and Avalanches
        * Erosion and Sediment Transport
    * Natural Disasters and Extreme Events
        * Earthquakes
        * Volcanic Eruptions
        * Storms and Hurricanes
* Astro-Physical and Cosmic Dynamics
    * Celestial Motion
        * Orbital Mechanics
        * Tidal Forces
    * Cosmic Phenomena
        * Supernovae
        * Meteor Showers
# Causes
* External Forces
    * Gravity
    * Friction
    * Buoyancy
    * Tension Force
    * Surface Tension
    * Compression
    * Elastic Force
* Internal Energy
    * Biological Activity
    * Mechanical Activity
* Heat Transfer
    * Conduction
    * Convection
    * Radiation
'''.strip()


# =============================================


DESC_PROMPT = '''
Please generate a comprehensive description of the video content. Include:  
1. subjects
2. motions
3. notable objects

Focus on conciseness while maintaining analytical depth. 
'''.strip()


# =============================================


CLS_AND_REASON_PROMPT = '''
## Objective
Classify the described video using the provided physical dynamics ontology. Output applicable categories with reasoning based on the description. If no category fits, output "Null".

## Ontology Structure
{ontology}

## Dense video description
{description}

## Output Format Guidelines

### Classification
List ALL applicable ontology categories as comma-separated values

If multiple independent categories apply, list them separately

### Reasoning
Explicitly connect description elements to chosen categories

Use concise, evidence-based explanations

### Null Condition
Only output Null if no category (including all subcategories) matches

## Output Examples

### Example 1
Class:  
Solid, Solid Motion, Solid, External Forces  

Reason:  
The rotating ball indicates solid motion (rotation). Collision demonstrates external forces (impact). 

### Example 2
Class:  
Human, Other Animals, Biological and Biomechanical Motion, Biological Activity

Reason:
this video is about a person playing with his pet dog.

### Example 3
Null
'''.strip()

