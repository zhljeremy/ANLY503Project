trace1 <- list(
  x = c(1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 
        2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017), 
  y = c(3.47654320988, 3.56145251397, 3.5166163142, 3.45921450151, 3.62080536913, 3.63503649635, 
        3.775, 3.55555555556, 3.53086419753, 3.26086956522, 3.24817518248, 3.144, 3.16666666667, 
        3.08646616541, 2.89015151515, 2.97202797203, 3.12418300654, 2.87412587413, 2.98, 2.99335548173, 
        3.1619047619, 3.0608974359, 2.972, 2.80608365019, 2.77559055118, 2.66064981949, 2.65925925926, 2.4701986755), 
  line = list(
    color = "rgb(22, 96, 167)", 
    width = 4
  ), 
  mode = "lines+markers", 
  name = "Top 50 Songs", 
  type = "scatter", 
  xsrc = "lufeiwang:46:4b5bdd", 
  ysrc = "lufeiwang:46:53d10b"
)
trace2 <- list(
  x = c(1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 
        2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017), 
  y = c(3.63235294118, 3.94117647059, 4.26666666667, 3.16666666667, 4.3, 4.125, 4.65384615385, 4.18571428571, 
        3.0987654321, 3.57142857143, 2.93333333333, 2.55555555556, 2.88888888889, 3.125, 2.75, 3.6, 3.74074074074, 
        3.75, 2.9375, 2.85714285714, 3.3164556962, 3.125, 2.9512195122, 2.62068965517, 2.89130434783, 2.79069767442,
        2.375, 2.28571428571), 
  line = list(
    color = "rgb(205, 12, 24)", 
    dash = "dash", 
    width = 4
  ), 
  mode = "lines+markers", 
  name = "Bottom 50 Songs", 
  type = "scatter", 
  xsrc = "lufeiwang:46:4b5bdd", 
  ysrc = "lufeiwang:46:5c9e0c"
)
data <- list(trace1, trace2)
layout <- list(
  title = "Average Length of Song Names, 1990 to 2017", 
  xaxis = list(title = "Years"), 
  yaxis = list(title = "Length")
)
p <- plot_ly()
p <- add_trace(p, x=trace1$x, y=trace1$y, line=trace1$line, mode=trace1$mode, name=trace1$name, type=trace1$type, xsrc=trace1$xsrc, ysrc=trace1$ysrc)
p <- add_trace(p, x=trace2$x, y=trace2$y, line=trace2$line, mode=trace2$mode, name=trace2$name, type=trace2$type, xsrc=trace2$xsrc, ysrc=trace2$ysrc)
p <- layout(p, title=layout$title, xaxis=layout$xaxis, yaxis=layout$yaxis)
p