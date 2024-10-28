from PickleManager import unique_urls_manager, subdomain_manager, token_manager

unique_urls_manager._RESET = False
subdomain_manager._RESET = False
token_manager._RESET = False

print("---- Report ----")
amount_of_urls = len(unique_urls_manager.unpickle_tokens())
print(f"\nThe amount of unique urls found where: {amount_of_urls}\n")
print("\n Most popular subdomains")
for k,v in subdomain_manager.unpickle_tokens().items():
    print(f"{k:30}:{v}")
print()
print("Here are some tokens")
count = 0
for k,v in token_manager.unpickle_tokens().items():
    if count > 50:
        break
    print(f"{k:30}:{v}")
    count += 1