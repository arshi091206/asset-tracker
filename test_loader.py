from alerts.asset_loader import get_asset,search_assets

print("---single lookup---")
print(get_asset("Infosys"))
print("---search results---")
results=search_assets("inf")
for asset in results:
    print(asset)