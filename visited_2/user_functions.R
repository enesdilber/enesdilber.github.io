get_wiki_URL = function(name){
  
  library(xml2)
  library(rvest)
  
  name = gsub(pattern = " ", replacement = "%20", x = name)
  
  google_search = read_html(
    x = paste0("https://www.google.com/search?q=Wikipedia%20", name))
  
  links = google_search %>% 
    html_nodes("cite") %>% # get the a nodes with an r class
    html_text() # get the urls
  
  return(links[1])
  
}

get_wiki_Loc = function(wiki_html, name){
  
  library(rvest)
  
  latlon = wiki_html %>% html_node(".geo-dec") %>% html_text()
  latlon = unlist(strsplit(latlon, " "))
  
  latlon = sapply(latlon, function(x){
    coor = as.numeric(gsub("N|E|W|S|°", "", x))
    len = nchar(x)
    ifelse(substr(x, len, len) %in% c("N", "E"), coor, -1*coor)
  })
  
  Latitude  = latlon[1]
  Longitude = latlon[2]
  
  # if there is no location info on wiki page, search open map:
  if(is.na(Latitude)){
    
    library(nominatim)
    
    temp = bb_lookup(name)
    tourism = which(temp$class == "tourism")
    loc_indx = ifelse(length(tourism) == 0, 1, tourism[1])
    
    Latitude  = as.numeric(temp$lat[1])
    Longitude = as.numeric(temp$lon[1])
  }
  
  return(list('Latitude' = Latitude, 'Longitude' = Longitude))
  
}

get_wiki_Descr = function(wiki_html, url, name){
  
  library(XML)

  doc = htmlParse(wiki_html, asText=TRUE)
  plain.text = xpathSApply(doc, "//p", xmlValue)
  
  mytext = ""; i = 1
  
  while(nchar(mytext)<20){
    mytext = plain.text[i]
    i = i + 1
  }
  
  Header = paste0("<b><a href='", url, "'target='_blank'>", name, "</a></b><br>")
  
  return(paste0(Header, mytext))
}

save_wiki_image = function(wiki_html, name, size, folder = NULL){
  
  library(RCurl)
  library(magick)
  
  wiki_imageurls = wiki_html %>% html_nodes(xpath = "//td/a") %>% html_attr("href")
  main_imageurl = which(sapply(wiki_imageurls, function(x) grepl("wiki/File:", x)))
  main_imageurl = ifelse(length(main_imageurl) == 0,
                         wiki_imageurls[1], wiki_imageurls[main_imageurl])
  main_imageurl = paste0("https://en.wikipedia.org", main_imageurl)
  wikipage = read_html(main_imageurl)
  imgurl = wikipage %>% html_node(".internal") %>% html_attr("href")
  main_imageurl = imgurl[1]
  
  imgurl = paste0("https:", main_imageurl)
  
  if(!url.exists(imgurl)){
    
    message("Looks like wikipedia page doesn't have a vcard now trying other images\n")
    
    library(rvest)
    library(xml2)
    
    wiki_imageurls = wiki_html %>% html_node(".thumbimage") %>% html_attr("src")
    tmp = gregexpr("/", wiki_imageurls)[[1]]
    main_imageurl = substr(wiki_imageurls, 1, tmp[length(tmp)]-1)
    main_imageurl = gsub(pattern = "thumb/", replacement = "", x = main_imageurl)
    
    imgurl = paste0("https:", main_imageurl)
    
    if(!url.exists(imgurl)){
      message("No wikipedia images found")
      return(0)
    }
    
  }
  
  last_dot = regexpr("\\.[^\\.]*$", imgurl) 
  #extension = substr(imgurl, last_dot, nchar(imgurl))
  extension = ".png"
  destination = ifelse(is.null(folder), 
                       paste0(name, extension),
                       paste0(folder, "/", name, extension))
  
  myimg = image_read(imgurl)
  myimg = image_scale(myimg, size)
  myimg = image_convert(myimg, "png")
  
  image_write(myimg, path = destination)
  
  return(destination)
  
}



