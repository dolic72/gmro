library(ROpenWeatherMap)
library(data.table)

api <- 'a45ab546f4d17be07dbd2006adc1cf08'
cid <- '2844988' # Rosenheim

w <- get_current_weather(api_key = api, cityID = cid)

w.out <- data.table(
  weather.cat = w$weather$main,
  weather.desc = w$weather$description,
  temperature.c = w$main$temp - 272.15,
  pressure.hpa = w$main$pressure, 
  humidity.pct = w$main$humidity,
  wind.speed.ms = w$wind$speed,
  wind.dir.deg = w$wind$deg,
  cloudiness.pct = w$clouds$all,
  dt = as.Date(as.POSIXct(w$dt, origin = "1970-01-01")),
  tm.n = as.numeric(format(as.POSIXct(w$dt, origin = "1970-01-01"), '%H%M')),
  tm.c = format(as.POSIXct(w$dt, origin = "1970-01-01"), '%H%M'),
  sunrise.dt = as.POSIXct(w$sys$sunrise, origin = "1970-01-01"),
  sunset.dt = as.POSIXct(w$sys$sunset, origin = "1970-01-01")
)

write.table(w.out, file = "/home/dolic/owm.csv", 
            append = TRUE, 
            row.names = FALSE, 
            col.names = FALSE,
            sep = ";",
            eol = "\n")