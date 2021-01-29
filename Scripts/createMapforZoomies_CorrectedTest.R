#### Init ####
if (1>0) {
  require(maps)
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
  
  usa <- map("state", fill = F, plot = T,
             regions = myStates)
  usa <- data.frame(x = usa[[1]],
                    y = usa[[2]])
  addCuba <- map("world", regions = "cuba", plot=F)
  addCuba <- data.frame(x = addCuba$x,
                        y = addCuba$y)
  addMex <- map("world", regions = "mexico", plot=F)
  addMex <- data.frame(x = addMex$x,
                       y = addMex$y)
  
  
  #Find southern border of Louisana to get coordinates for plotting towns
  myLA <- c("louisiana")
  usa2 <- map("state", fill = F, plot = F,
              regions = myLA)
  usa2 <- data.frame(x = usa2[[1]],
                     y = usa2[[2]])
  
  coastCoords <- usa2[which(usa2$y < 29.8),]
  
  #Find easter border of Texas to get coordinates for plotting towns
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
  points(coastCoords$x, coastCoords$y, col="blue", pch=19)
  
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

currAng <- 75
currSD <- 20

zoomies$ang <- rnorm(numZoomies, currAng, currSD)

coneLen <- 6
x1 <- -90
y1 <- 22
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


#### Zach - I stopped here ####

#sohcahtoa

####  Set up Zoomies ####
fnBase <- "zoomieUp"

stX <- -90
stY <- 22
points(stX,stY, pch=19)
endY <- 28
moveDist <- endY - stY

zoomieSize <- 3
numZoomies <- 50
numMoves <- moveDist #Number of times the zoomies move
numMovesCone <- moveDist*1.2  #cone "moves" farther bc no random variation
imgNum <- 0 #used to create image names
i <- 1  #used for testing only

#highRiskThreshold <- 5  #for use when coloring zoomies (later)
#colfunc <- colorRampPalette(brewer.pal(9,"Purples"))  #for use when coloring zoomies (later)
#colfuncRed <- colorRampPalette(brewer.pal(9,"Reds"))  #for use when coloring zoomies (later)

#how much each zoomie moves in x/y directions at each move
deltaX <- c(0, .8, .6, .4, -.4)
deltaY <- c(1, .6, .8, .92, .92)

#how much each zoomie moves in x/y directions at each move
possibleAngles <- c(90, 110, 70, 50, 30)

for (myAng in 1:length(deltaX)) {
  for (mySD in c(.1,.15,.2,.25)) {  
    #    for(townPos in seq(-5,5)) {
    
    #### Set it Up ####
    imgNum <- imgNum + 1
    
    ## Set up Zoomies
    dt <- data.frame(zoomie = seq(1,numZoomies),
                     y = rnorm(numZoomies,deltaY[myAng], .05),  #average upwards travel = 1
                     x = rnorm(numZoomies,deltaX[myAng],mySD),  #.1 does about 1/3  .2 covers nearly everything
                     col = rep(1,numZoomies),
                     sz = rep(zoomieSize,numZoomies))
    
    ## Set Town Location
    townIndex <- round(runif(1, 1, dim(coastCoords)[1]))
    
    #### Draw Each Frame ####
    #  for (i in 0:numMoves) {  #comment out if want to draw them all at once
    
    #Start Figure
    fn <- paste0(fnBase,imgNum,"-",i,"EX",".png")
    #   png(fn, width = 480, height = 400)
    par(mar=c(.1,.1,.1,.1))
    
    #Plot Map
    plot(usa$x, usa$y, type = "l", bty="n", xaxt="n", yaxt="n", xlab="",ylab="", 
         xlim=c(-100, -80), ylim=c(22, 32))  #ylim was 15
    lines(addCuba$x, addCuba$y)
    lines(addMex$x, addMex$y)
    
    ## Add Zoomies
    for (i in 0:numMoves) {
      for (j in 1:numZoomies) {
        a <- which(dt$zoomie == j)
        x <- i * dt$x[a] + stX
        y <- i * dt$y[a] + stY
        points(x,y,col = dt$col[a],
               pch=15)
      } #end plot each zoomie
    }
    
    #### Select and Add Town ####
    ## Select Town (based on townPos)
    tRange <- .4
    tAdd <- 1.1
    for(townPos in seq(-5,5)) {
      
      if (townPos == 0) {
        #town in center
        midX <- deltaX[myAng] * numMoves
      } else if(townPos == 1) {
        midX <- (deltaX[myAng] + mySD*.33) * numMovesCone*tAdd
      } else if(townPos == 2) {
        midX <- (deltaX[myAng] + mySD*.67) * numMovesCone*tAdd
      } else if(townPos == 3) {
        midX <- (deltaX[myAng] + mySD*.97) * numMovesCone*tAdd
      } else if(townPos == 4) {
        midX <- (deltaX[myAng] + mySD*1.5) * numMovesCone*tAdd
      } else if(townPos == 5) {
        midX <- (deltaX[myAng] + mySD*2) * numMovesCone*tAdd
      } else if(townPos == -1) {
        midX <- (deltaX[myAng] - mySD*.33) * numMovesCone*tAdd
      } else if(townPos == -2) {
        midX <- (deltaX[myAng] - mySD*.67) * numMovesCone*tAdd
      } else if(townPos == -3) {
        midX <- (deltaX[myAng] - mySD*.97) * numMovesCone*tAdd
      } else if(townPos == -4) {
        midX <- (deltaX[myAng] - mySD*1.5) * numMovesCone*tAdd
      } else if(townPos == -5) {
        midX <- (deltaX[myAng] - mySD*2) * numMovesCone*tAdd
      }
      midX <- midX + stX
      
      a <- which(coastCoords$x > (midX - tRange) & 
                   coastCoords$x < (midX + tRange))
      if (length(a) < 2) {
        a <- which(coastCoords$x > (midX - tRange*1.2) & 
                     coastCoords$x < (midX + tRange*1.2))
        
      }
      townIndex <- a[round(runif(1,1,length(a)))]
      
      
      
      ## Add Town
      points(coastCoords$x[townIndex], coastCoords$y[townIndex], pch = 19, cex=2, col=rainbow(11, end=.8)[townPos + 6])
      
      
      
      
      #### Add Cone ####
      coneLWD <- 2
      numMovesCone <- 1.2 * numMoves
      
      ## center of cone
      coneXs <- stX + seq(0,numMovesCone,length.out = 4) * deltaX[myAng]  #points at center of cone
      coneYs <- stY + seq(0,numMovesCone,length.out = 4) * deltaY[myAng]  #points at center of cone
      points(coneXs, coneYs, pch=19, cex=2, col = "gray")
      points(x = stX, y=stY, pch=1, cex=3)
      
      for (i in 1:3) {
        segments(coneXs[i],coneYs[i], coneXs[i+1],coneYs[i+1])
      }
      
      ## Edges of cone
      x1 <- stX * deltaX[myAng]
      y1 <- stY * deltaY[myAng]
      currAng = possibleAngles[myAng]
      currSD = mySD
      x2 <- cos(currAng / 180 * pi) * coneLWD + x1
      y2 <- sin(currAng / 180 * pi) * coneLWD + y1
      segments(x1,y1,x2,y2, xpd=NA)
      
      myRadius = tan(currSD / 180 * pi) * coneLWD     
      
      x3 <- x2 + cos((90-currAng) / 180 * pi) * myRadius
      y3 <- y2 - sin((90-currAng) / 180 * pi) * myRadius
      segments(x1,y1,x3,y3, xpd=NA, lwd=coneLWD)
      
      x4 <- x2 - cos((90-currAng) / 180 * pi) * myRadius
      y4 <- y2 + sin((90-currAng) / 180 * pi) * myRadius
      segments(x1,y1,x4,y4, xpd=NA, lwd=coneLWD)
      
      plotrix::draw.arc(x2,y2,myRadius,angle2 = (currAng + 90)/180*pi, 
                        angle1 = (currAng - 90)/180*pi, col="blue")
      
      
      
      
      #    dev.off()
      
      #  } #end plot each move
      
      if(1>2) {
        #### Create Animation ####
        ii <- 1
        img <- image_read(paste0(fnBase,imgNum,"-",ii,"EX.png"))
        for (ii in 2:numMoves) {
          img <- c(img,image_read(paste0(fnBase,imgNum,"-",ii,"EX.png")))
        }
        
        image_info(img)
        
        #  animation <- image_animate(image_scale(img, "400x400"), fps = 100, dispose = "previous")
        animation <- image_animate(image_scale(img, "400x400"), delay = .3, dispose = "previous", loop = 0)
        image_write(animation, paste0(fnBase,imgNum,".gif"))
        
        #### Clean Up - Optional ####
        
        # Remove .png files after animation
        file.remove(list.files(pattern="EX.png"))
        
        
      } #end if for checking
      
    } #end for each townPos
  } #end plot each set
} #end plot each angle

