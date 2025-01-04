# Readme

Python script that sets hynocube LEDs according to current and upcoming weather variability

# Change LED patterns based on

- Current temperature
- Variation in temperature over next 6 hours
- Percipitation (current and future)
- Wind

# Example

Values between 0 and 1

{t:{$current,$min,$max}}
{w:{$current,$min,$max}}
{p:{$current,$worst}}

perciptation enums:
sunny,partlycloudy,cloudy,rain,intenseRain,snow,intenseSnow
