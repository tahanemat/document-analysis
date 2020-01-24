FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

FROM mcr.microsoft.com/dotnet/core/runtime:3.1

COPY ProdCon/bin/Release/netcoreapp3.1/publish/ app/

ENTRYPOINT ["dotnet", "app/ProdCon.dll"]