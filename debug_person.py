from models.person import Person

p = Person(
    full_name="Test User",
    profile_url="https://google.com",
    image_url="image.jpg"
)

print(p)
print("profile_url =", p.profile_url)
print("image_url   =", p.image_url)