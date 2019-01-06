library(readr)
library(leaflet)
library(htmlwidgets)

places = read_csv("output/places.csv")

icons <- awesomeIcons(
  icon = 'ios-close',
  iconColor = 'black',
  library = 'ion',
  markerColor = ifelse(places$isvisited, "green", "red"))

m = leaflet(data = places) %>% 
  addTiles() %>%
  addAwesomeMarkers(lng = ~Longitude, 
                    lat = ~Latitude, 
                    label = ~Name,
                    popup = ~Info, 
                    icon = icons,
                    clusterOptions = markerClusterOptions())

saveWidget(m, file="m.html", selfcontained = F)