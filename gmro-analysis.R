library(ggplot2)
library(reshape2)
library(data.table)
library(sp)

pfad <- "/home/dolic/"

raw <- read.csv(file.path(pfad, "gmro-count.csv"),
                colClasses = c("character", "character", "numeric", "character", "numeric"))

r <- raw[raw$X == "rot", -5]
g <- raw[raw$X == "gruen", -5]

names(r) <- c("farbe", "datum", "red", "zeit")
names(g) <- c("farbe", "datum", "green", "zeit")

g <- g[-1]
r <- r[-1]

rg <- merge(r, g)


daylevels <- switch(Sys.getlocale(category = "LC_TIME"), 
                    "en_US.UTF-8" = c("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"), 
                    "German_Germany.1252" = c("Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"))

df <- data.table(
  dt = as.Date(as.character(rg$datum), '%Y%m%d'),
  tm = factor(as.character(rg$zeit)),
  tm.num = as.numeric(rg$zeit),
  dttm = as.POSIXct(strptime(paste(rg$datum, rg$zeit), '%Y%m%d %H%M')),
  tag = factor(format(as.Date(rg$datum, '%Y%m%d'), "%a"),
               levels = daylevels),
  num.monat = factor(format(as.Date(rg$datum, '%Y%m%d'), "%m"),
                     levels = format(seq(as.Date("2015-01-01"), as.Date("2015-12-31"),"month"), "%m")),
  nam.monat = factor(format(as.Date(rg$datum, '%Y%m%d'), "%b"),
                     levels = format(seq(as.Date("2015-01-01"), as.Date("2015-12-31"),"month"), "%b")),
  red = rg$red,
  green = rg$green,
  sum.rg = rg$red + rg$green,
  red.pct = rg$red/(rg$red + rg$green),
  green.pct = rg$green/(rg$red + rg$green),
  red.ratio = rg$red/rg$green
)

# data cleaning
df <- df[order(df$dttm),]
df <- df[df$dt >= as.Date("2016-10-21"),]
df <- df[df$tm.num %% 5 == 0, ]

to.plot <- df[df$tm.num > 600,]

jpeg(filename = file.path(pfad, "boxplot-tag-stunde.jpg"), width = 1200, height = 600)
p <- ggplot(df, aes(tm, red))
p + geom_boxplot(colour = "#ffd700", fill = "#9A0000") + facet_grid(. ~ tag) + 
  labs(x = "", y = "") +
  theme(axis.ticks = element_blank(), axis.text.y = element_blank())
dev.off()

jpeg(filename = file.path(pfad, "bp-per-wochentag.jpg"), width = 1200, height = 400)
p <- ggplot(df, aes(tag, red))
p + geom_boxplot(fill = "red") + 
  xlab("Wochentag") + ylab("")
dev.off()

jpeg(filename = file.path(pfad, "heatmap-tag-stunde.jpg"), width = 400, height = 1200)
to.plot <- to.plot[to.plot$red.pct < 0.8, ]
ggplot(to.plot, aes(tag, tm, fill = red)) + 
  geom_raster() + 
  scale_fill_gradient(low = "#bfffbf", high = "#9A0000") +
  labs(x = "", y = "") +
  guides(fill = FALSE)
dev.off()

mn.red <- aggregate(red ~ tag + tm, data = df, mean)

p <- ggplot(mn.red, aes(tm, red))
p + geom_boxplot() + facet_grid(. ~ tag)

############# Coordinates #################
library(dbscan)
library(GISTools)
library(png)
library(grid)

raw <- read.csv(file.path(pfad, "gmro-coord.csv"),
                colClasses = c("numeric", "character", "character", "character", "numeric", "numeric"))

rot <- raw[raw$Farbe == "rot",]


red.cord.dt <- data.table(
  dt = as.Date(as.character(rot$Datum), '%Y%m%d'),
  tm = factor(as.character(rot$Zeit)),
  tm.num = as.numeric(rot$Zeit),
  dttm = as.POSIXct(strptime(paste(rot$Datum, rot$Zeit), '%Y%m%d %H%M')),
  tag = factor(format(as.Date(rot$Datum, '%Y%m%d'), "%a"),
               levels = daylevels),
  num.monat = factor(format(as.Date(rot$Datum, '%Y%m%d'), "%m"),
                     levels = format(seq(as.Date("2015-01-01"), as.Date("2015-12-31"),"month"), "%m")),
  nam.monat = factor(format(as.Date(rot$Datum, '%Y%m%d'), "%b"),
                     levels = format(seq(as.Date("2015-01-01"), as.Date("2015-12-31"),"month"), "%b")),
  lon = rot$lon,
  lat = rot$lat
)

rm(raw)

## GIStools
red.cord.sp <- red.cord.dt
coordinates(red.cord.sp) <- ~lon+lat
hotpots <- kde.points(red.cord.sp)

## DBSCAN
res <- dbscan(as.matrix(red.cord.dt$lon, red.cord.dt$lat), eps = 100, minPts = 10)

# One day only
x <- red.cord.dt[red.cord.dt$dt == as.Date("2017-02-07"), list(lon, lat)]
res <- dbscan(x, eps = 100, minPts = 10)
toplot <- cbind(x, res$cluster)
ggplot(toplot, aes(lon, lat)) + geom_point(aes(colour = factor(V2)))

## Time-specific
x <- red.cord.dt[red.cord.dt$tag == "Fri"
                   & red.cord.dt$tm.num > 700 
                   & red.cord.dt$tm.num < 830
                   # & red.cord.dt$num.monat == "02"
                 , list(lon, lat)]

x <- x[!x$lat %in% 700:740 & !x$lon %in% 760:766,]

m <- ggplot(x, aes(lon, lat)) + geom_point()
m + stat_density_2d(aes(fill = ..level..), geom = "polygon")

ggplot(x, aes(lon, lat)) + geom_bin2d()

bg <- readPNG("/home/dolic/gmro/gmroproc/gmro-20170207050001.png")

ggplot(x, aes(lat, abs(800-lon))) + 
  annotation_custom(rasterGrob(bg, x = unit(0.5, "npc"), y = unit(0.5, "npc"),
                               width = unit(1, "npc"), height = unit(1, "npc")), 
                    xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=Inf) + 
  geom_point(color = "#f9b5b3", size = 0.5) +
  stat_density_2d(aes(fill = ..level..), geom = "polygon") + 
  scale_fill_gradient(low="#f9b5b3", high="#ff0400") +
  scale_x_continuous(limits = c(0, 1280), expand = c(0,0)) +
  scale_y_continuous(limits = c(0, 800), expand = c(0,0)) 

## bin
ggplot(x, aes(lat, (800-lon))) +
  annotation_custom(rasterGrob(bg, x = unit(0.5, "npc"), y = unit(0.5, "npc"),
                               width = unit(1, "npc"), height = unit(1, "npc")), 
                    xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=Inf) +
  geom_bin2d(bins = 100) +
  scale_fill_gradient(low="#ffdbdb", high="#c40000", name = "Häufigkeit") +
  scale_x_continuous(limits = c(0, 1280), expand = c(0,0), labels = NULL, breaks = NULL, name = NULL) +
  scale_y_continuous(limits = c(0, 800), expand = c(0,0), labels = NULL, breaks = NULL, name = NULL) 


# Unbusy time
x <- red.cord.dt[red.cord.dt$tag == "Tue"
                 & red.cord.dt$tm.num > 1530 
                 & red.cord.dt$tm.num < 1700
                 , list(lon, lat)]
x <- x[!x$lat %in% 700:740 & !x$lon %in% 760:766,]
ggplot(x, aes(lat, (800-lon))) +
  annotation_custom(rasterGrob(bg, x = unit(0.5, "npc"), y = unit(0.5, "npc"),
                               width = unit(1, "npc"), height = unit(1, "npc")), 
                    xmin=-Inf, xmax=Inf, ymin=-Inf, ymax=Inf) +
  geom_bin2d(bins = 100) +
  scale_fill_gradient(low="#ffdbdb", high="#c40000", name = "Häufigkeit") +
  scale_x_continuous(limits = c(0, 1280), expand = c(0,0), labels = NULL, breaks = NULL, name = NULL) +
  scale_y_continuous(limits = c(0, 800), expand = c(0,0), labels = NULL, breaks = NULL, name = NULL) 


## Read weather
w <- read.table(file.path(pfad, "owm.csv"))

### Time series
d <- df[df$dt > as.Date("2016-12-31"),]

ggplot(d, aes(dttm, red.pct)) +
  geom_line(color = "#ff8d6d") +
  geom_smooth(method = "loess") + 
  labs(title = "Anteil im Zeitverlauf", x = "", y = "Anteil Verkehrsstörungen (px)")