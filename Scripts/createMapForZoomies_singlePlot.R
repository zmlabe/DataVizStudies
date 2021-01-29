#### Init ####
if (1>0) {
  require(maps)
  require(mapproj)
  require(viridis)
  require(RColorBrewer)
  require(magick)
  require(plotrix)
  
  setwd("/Users/zlabe/Documents/Research/Visualizations/")
  
  set.seed(90210)
  
}

#### Grab States ####
if(1>0) {
  
  myStates <- c("louisiana","mississippi","alabama","georgia","texas","florida")
  
  usa <- map("state",fill = F, plot = T,
             regions = myStates, resolution = 0)
  usa <- data.frame(x = usa[[1]],
                    y = usa[[2]])
 addCuba <- map("world", regions = "cuba", plot=T,add=T)
 addCuba <- data.frame(x = addCuba$x,
                         y = addCuba$y)
  addMex <- map("world", regions = "mexico", plot=T,add=T)
  addMex <- data.frame(x = addMex$x,
                        y = addMex$y)
  
  
  #Find southern border of Louisiana to get coordinates for plotting towns
  myLA <- c("louisiana")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  
  coastCoords <- usa2[which(usa2$y < 29.8),]
  
  #Find eastern border of Texas to get coordinates for plotting towns
  myLA <- c("texas")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  coastCoords <- rbind(coastCoords,usa2[which(usa2$y < 29.8 & usa2$x > -97),])
  
  myLA <- c("florida")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  coastCoords <- rbind(coastCoords,usa2[which(usa2$x < -81.2 & usa2$y < 29.5),])
  coastCoords <- rbind(coastCoords,usa2[which(usa2$x < -85 & usa2$y < 30.45),])
  coastCoords <- rbind(coastCoords,usa2[which(usa2$x > -85.5 & usa2$x < -83 & usa2$y < 30.3),])
  
  myLA <- c("alabama")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  a <- which(usa2$y < 30.4)
  coastCoords <- rbind(coastCoords,usa2[a,])
  
  myLA <- c("mississippi")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  a <- which(usa2$y < 30.45 & usa2$x > -89.5)
  coastCoords <- rbind(coastCoords,usa2[a,])
  
  
  coastCoords <- coastCoords[rank(coastCoords$x),]
  #points(coastCoords$x, coastCoords$y, col="blue", pch=19)
  
} #end set it up  


#### Try one ####

numZoomies <- 50
zoomies <- data.frame(ang = NA,
                      deltaX = NA,
                      deltaY = NA,
                      col = "black",
                      size = 3)
zoomies[1:numZoomies,] <- NA
zoomies$col <- "black"
zoomies$size <- 3

currAng <- 80
currSD <- 20

zoomies$ang <- rnorm(numZoomies, currAng, currSD)

coneLen <- 6
x1 <- -90
y1 <- 24
x2 <- cos(currAng / 180 * pi) * coneLen + x1
y2 <- sin(currAng / 180 * pi) * coneLen + y1
segments(x1,y1,x2,y2, xpd=NA)

myRadius = tan(currSD / 180 * pi) * coneLen


x3 <- x2 + cos((90-currAng) / 180 * pi) * myRadius
y3 <- y2 - sin((90-currAng) / 180 * pi) * myRadius
segments(x1,y1,x3,y3, xpd=NA, lwd=1)

x4 <- x2 - cos((90-currAng) / 180 * pi) * myRadius
y4 <- y2 + sin((90-currAng) / 180 * pi) * myRadius
segments(x1,y1,x4,y4, xpd=NA, lwd=1)

plotrix::draw.arc(x2,y2,myRadius,angle2 = (currAng + 90)/180*pi, angle1 = (currAng - 90)/180*pi, col="blue")