# Use the pet store

def psclient(store):
    for name in "Alvin Bob Carly Diana".split():
        store.addPet(name)
    for name in "Spot Crookshanks Mrs.Norris Jinx".split():
        store.addPet(name, "cat")
    for name in "Fido Rover Astro Scooby".split():
        store.addPet(name, "dog")
    store.addPet("Hedwig", "bird")

    print "All", store.findPets()
    print "Ten", store.findPets(limit=10)
    print "Cats", store.findPets(tags=["cat"])
    print "Uncats", store.findPets(tags=[None])
    print "Quads", store.findPets(tags="cat dog".split())

    print store.findPetById(3)
    store.deletePet(3)
    print "Uncats", store.findPets(tags=[None])
    try:
        print store.findPetById(3)
    except LookupError:
        print "Got expected exception"


def main():
    import petstore
    store = petstore.PetStore()
    psclient(store)

def main2():
    from adaptive import sample_rpc
    store = sample_rpc.Client("http://127.0.0.1:8080/PetStore")
    psclient(store)


if __name__ == "__main__":
    main()
    print "===" * 30
    main2()