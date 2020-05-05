using Distributed, CSV, Plots, TimeSeries, CSV.DataFrames;
using Plots.PlotMeasures
ENV["DRIVER_SCRIPT"] = @__FILE__

cd(@__DIR__)
cd(dirname(pwd()))


include("./data/create_cmd.jl") #what's the directory structure?

@everywhere using CSV, Dates, CSV.DataFrames;
@everywhere function convert2df(x)
   run(x)
   fname = split(x[2], "/")[end]
   df = DataFrame(CSV.read(fname))
   sort!(df, :Date)
   yearly_df = DataFrame(Date=df[:,:Date][1],Open=df[:,:Open][1],High=maximum(df[:,:High]),Low=minimum(df[:, :Low]),Close=df[:,:Close][end] )
end

df = vcat(pmap(convert2df, wget_cmds)...)
df = TimeArray(df[[:Date, :Open, :High, :Low, :Close]], timestamp=:Date)
plot(df, st = :heikinashi, color = [:red, :blue], xlabel="Year\n", ylabel="Price", title="Apple Stock Price", left_margin =10mm,top_margin =10mm,bottom_margin =10mm)
savefig("ohlc.png")
ENV["RESULTS_FILE_TO_UPLOAD"] = "ohlc.png"
