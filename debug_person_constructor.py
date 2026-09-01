from inspect import signature
from models.person import Person

print("Constructor:")
print(signature(Person))

print()

p = Person(
    full_name="John Doe",
    profile_url="https://google.com",
    image_url="image.jpg",
)

print("repr:", p)
print()

print("dict:")
print(vars(p))
print()

print("profile_url:", p.profile_url)
print("image_url:", p.image_url)