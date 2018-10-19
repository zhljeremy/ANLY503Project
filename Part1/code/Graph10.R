trace1 <- list(
  x = c(1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 
        2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017), 
  y = c(3.47654320988, 3.56145251397, 3.5166163142, 3.45921450151, 3.62080536913, 3.63503649635, 3.775, 
        3.55555555556, 3.53086419753, 3.26086956522, 3.24817518248, 3.144, 3.16666666667, 3.08646616541, 
        2.89015151515, 2.97202797203, 3.12418300654, 2.87412587413, 2.98, 2.99335548173, 3.1619047619, 
        3.0608974359, 2.972, 2.80608365019, 2.77559055118, 2.66064981949, 2.65925925926, 2.4701986755), 
  line = list(
    color = "rgb(22, 96, 167)", 
    width = 4
  ), 
  mode = "lines+markers", 
  name = "Average Length of Song Names", 
  type = "scatter", 
  xsrc = "lufeiwang:40:a32ddd", 
  ysrc = "lufeiwang:40:ac88e4"
)
data <- list(trace1)
layout <- list(
  title = "Average Length of Song Names, 1990 to 2017", 
  xaxis = list(title = "Year"), 
  yaxis = list(title = "Length")
)
p <- plot_ly()
p <- add_trace(p, x=trace1$x, y=trace1$y, line=trace1$line, mode=trace1$mode, name=trace1$name, type=trace1$type, xsrc=trace1$xsrc, ysrc=trace1$ysrc)
p <- layout(p, title=layout$title, xaxis=layout$xaxis, yaxis=layout$yaxis)
p