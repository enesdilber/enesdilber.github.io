source("user_functions.R")

# not visited yet
not_visited = readLines(file("input/wanna_visit.txt"))

# visited already
photo_names = unname(
  sapply(list.files("input/my_photos/"), function(x){
    last_dot = regexpr("\\.[^\\.]*$", x) # find the file extention starting char
    tmp = substr(x, 1, last_dot-1) # remove the extension
    gsub('[0-9]+', '', tmp) # remove the numbers in name
  }))

visited = unique(photo_names) # ignore the duplicates
rm(photo_names)

Name = c(visited, not_visited)
places = data.frame(Name = Name,
                    Latitude = NA,
                    Longitude = NA,
                    Info = NA,
                    isvisited = c(rep(T, length(visited)), rep(F, length(not_visited))))

for(i in 1:length(Name)){
  name = Name[i]
  url = get_wiki_URL(name)
  
  message(paste0("--------------------------------------------------\nName:", name))
  message(paste0("--------------------------------------------------"))

  #############################################
  wiki_html = read_html(url)
  message("\nRead Wikipedia Page: Done")
  #############################################
  loc = get_wiki_Loc(wiki_html, name)
  places$Latitude[i] = loc$Latitude
  places$Longitude[i] = loc$Longitude
  message("\nLocation: Done")
  #############################################
  savedimage = save_wiki_image(wiki_html, name, "300", "output/wiki_photos")
  message("\nImage saved")
  #############################################
  Description = get_wiki_Descr(wiki_html, url, name)
  Description = paste0(Description, "<br><img src = ", savedimage, "><br>")
  
  if(places$isvisited[i]){
    my_photos = paste0("input/my_photos/", list.files("input/my_photos/", name))
    
    my_photos = paste(paste0('<a href="', my_photos,'"target="_blank"', 
                             ">Photo #", 1:length(my_photos), "</a>"), collapse = "<br>")
    Description = paste0(Description, "<br>", my_photos)
  }
  places$Info[i] = Description
  message("\nInfo: Done\n")
  #############################################
}

library(readr)
write_csv(places, "output/places.csv")
message("output/places.csv created")










