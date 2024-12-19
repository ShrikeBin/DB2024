//<[1.1]>-----------------------------------------------------------------------------------------------------------------------------------

use library

//<[1.2]>-----------------------------------------------------------------------------------------------------------------------------------

db.createCollection("authors", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["name", "country", "birth", "death"],
      properties: {
        name: {
          bsonType: "object",
          required: ["first", "last"],
          properties: {
            first: { bsonType: "string" },
            last: { bsonType: "string" }
          }
        },
        country: { bsonType: "string" },
        birth: { bsonType: "date" },
        death: { bsonType: ["date", "null"] }
      }
    }
  },
  validationAction: "error"
});

db.createCollection("books", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["title", "isbn", "publication_year", "language", "author", "publisher"],
      properties: {
        title: { bsonType: "string" },
        isbn: { bsonType: "string" },
        publication_year: { bsonType: "int" },
        language: { bsonType: "string" },
        author: { bsonType: "objectId" },
        publisher: {
          bsonType: "object",
          required: ["name", "country"],
          properties: {
            name: { bsonType: "string" },
            country: { bsonType: "string" }
          }
        }
      }
    }
  },
  validationAction: "error"
});

//<[1.3]>-----------------------------------------------------------------------------------------------------------------------------------

db.authors.insertMany([
  {
    name: { first: "Peter", last: "Watts" },
    country: "Canada",
    birth: new Date('1958-01-25'),
    death: null
  },
  {
    name: { first: "Stanisław", last: "Lem" },
    country: "Poland",
    birth: new Date('1921-09-12'),
    death: new Date('2006-03-27')
  },
  {
    name: { first: "Fiodor", last: "Dostojewski" },
    country: "Russia",
    birth: new Date('1821-10-30'),
    death: new Date('1881-01-28')
  },
  {
    name: { first: "Henryk", last: "Sienkiewicz" },
    country: "Poland",
    birth: new Date('1846-05-05'),
    death: new Date('1916-11-15')
  }
]);

db.books.insertMany([
  {
    title: "Ślepowidzenie",
    isbn: "978-83-67793-33-9",
    publication_year: 2006,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Watts" })._id,
    publisher: { name: "MAG", country: "Poland" }
  },
  {
    title: "Echopraksja",
    isbn: "978-83-68069-37-2",
    publication_year: 2024,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Watts" })._id,
    publisher: { name: "MAG", country: "Poland" }
  },
  {
    title: "Rozgwiazda",
    isbn: "978-83-7731-464-7",
    publication_year: 2023,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Watts" })._id,
    publisher: { name: "vesper", country: "Poland" }
  },
  {
    title: "Solaris",
    isbn: "978-83-207-1234-5",
    publication_year: 1961,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Lem" })._id,
    publisher: { name: "Czytelnik", country: "Poland" }
  },
  {
    title: "Dzienniki gwiazdowe",
    isbn: "978-83-207-1235-2",
    publication_year: 1957,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Lem" })._id,
    publisher: { name: "Czytelnik", country: "Poland" }
  },
  {
    title: "Bajki robotów",
    isbn: "978-83-207-1236-9",
    publication_year: 1964,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Lem" })._id,
    publisher: { name: "Czytelnik", country: "Poland" }
  },
  {
    title: "Zbrodnia i kara",
    isbn: "978-83-7508-0001-2",
    publication_year: 1887,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Dostojewski" })._id,
    publisher: { name: "Państwowy Instytut Wydawniczy", country: "Poland" }
  },
  {
    title: "Bracia Karamazow",
    isbn: "978-83-7508-0002-9",
    publication_year: 1880,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Dostojewski" })._id,
    publisher: { name: "Państwowy Instytut Wydawniczy", country: "Poland" }
  },
  {
    title: "Idiota",
    isbn: "978-83-7508-0003-6",
    publication_year: 1869,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Dostojewski" })._id,
    publisher: { name: "Państwowy Instytut Wydawniczy", country: "Poland" }
  },
  {
    title: "Quo Vadis",
    isbn: "978-83-7508-1001-2",
    publication_year: 1896,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Sienkiewicz" })._id,
    publisher: { name: "Gebethner i Wolff", country: "Poland" }
  },
  {
    title: "Krzyżacy",
    isbn: "978-83-7508-1002-9",
    publication_year: 1900,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Sienkiewicz" })._id,
    publisher: { name: "Gebethner i Wolff", country: "Poland" }
  },
  {
    title: "Ogniem i mieczem",
    isbn: "978-83-7508-1003-6",
    publication_year: 1884,
    language: "Polish",
    author: db.authors.findOne({ "name.last": "Sienkiewicz" })._id,
    publisher: { name: "Gebethner i Wolff", country: "Poland" }
  }
]);


//<[1.4]>-----------------------------------------------------------------------------------------------------------------------------------

db.createCollection("reviews", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["book", "reviewer", "rating", "review_text"],
      properties: {
        book: { bsonType: "objectId" },
        reviewer: {
          bsonType: "object",
          required: ["email", "nick"],
          properties: {
            email: { bsonType: "string" },
            nick: { bsonType: "string" }
          }
        },
        rating: {           
          bsonType: "int",
          minimum: 1,  
          maximum: 5   
          },
        review_text: { bsonType: "string" },
      }
    }
  },
  validationAction: "error"
});

db.reviews.insertMany([
    {
      book: db.books.findOne({ "title": "Ślepowidzenie" })._id,
      reviewer: {email: "jankowalski@gmail.com", nick: "Kovlasky"},
      rating: 4,
      review_text: "Nom dobra taka nie za prosta"
    },
    {
      book: db.books.findOne({ "title": "Ślepowidzenie" })._id,
      reviewer: { email: "bob@example.com", nick: "SciFiFan" },
      rating: 5,
      review_text: "A thrilling experience, full of mind-bending concepts."
    },
    {
      book: db.books.findOne({ "title": "Ślepowidzenie" })._id,
      reviewer: { email: "carol@example.com", nick: "FantasyKing" },
      rating: 1,
      review_text: "Unreasonably complicated garbage"
    },
    {
      book: db.books.findOne({ "title": "Ślepowidzenie" })._id,
      reviewer: { email: "derek@example.com", nick: "CyberpunkFan" },
      rating: 2,
      review_text: "not enough CYBERPUNK!"
    },
    {
      book: db.books.findOne({ "title": "Krzyżacy" })._id,
      reviewer: { email: "pawel@example.com", nick: "MrRouge" },
      rating: 5,
      review_text: "Arcydzieło polskiej literatury"
    },
      {
      book: db.books.findOne({ "title": "Quo Vadis" })._id,
      reviewer: { email: "pawel@example.com", nick: "MrRouge" },
      rating: 5,
      review_text: "Arcydzieło polskiej literatury"
    },
      {
      book: db.books.findOne({ "title": "Ogniem i mieczem" })._id,
      reviewer: { email: "pawel@example.com", nick: "MrRouge" },
      rating: 5,
      review_text: "Arcydzieło polskiej literatury"
    },
    {
      book: db.books.findOne({ "title": "Rozgwiazda" })._id,
      reviewer: { email: "pawel@example.com", nick: "MrRouge" },
      rating: 2,
      review_text: "Do quo vadis nie ma podjazdu"
    },
    {
      book: db.books.findOne({ "title": "Echopraksja" })._id,
      reviewer: { email: "pawel@example.com", nick: "MrRouge" },
      rating: 3,
      review_text: "Całkiem ciekawe jak na sci-fi"
    }
  ]);

//<[1.5]>-----------------------------------------------------------------------------------------------------------------------------------

db.authors.updateMany(
  {},
  {
    $set: {
      awards: [
        {
          name: "",    // Puste miejsce na nazwę nagrody
          date: ""     // Puste miejsce na datę otrzymania nagrody
        }
      ]
    }
  }
);

db.books.updateMany(
  {},
  {
    $set: { genres: [] }
  }
);

//<[1.6]>-----------------------------------------------------------------------------------------------------------------------------------

db.books.find({ 
    author: 
    db.authors.findOne({ 
        "name.first": "Peter", 
        "name.last": "Watts" })._id 
        }).pretty();


db.books.find({
    language: "Polish",
    genres: "Fantasy"
  }).pretty();


db.books.aggregate([
  {
    $lookup: {
      from: "reviews",
      localField: "_id",
      foreignField: "book",
      as: "book_reviews"
    }
  },
  {
    $addFields: {
      avgRating: { $avg: "$book_reviews.rating" }
    }
  },
  {
    $match: {
      avgRating: { $gte: 4 }
    }
  },
  {
    $project: {
      title: 1,
      avgRating: 1
    }
  }
]);


db.books.aggregate([
  {
    $lookup: {
      from: "authors",
      localField: "author",
      foreignField: "_id",
      as: "book_author"
    }
  },
  {
    $unwind: "$book_author"
  },
  {
    $match: {
      "book_author.country": "Poland"
    }
  },
  {
    $lookup: {
      from: "reviews",
      localField: "_id",
      foreignField: "book",
      as: "book_reviews"
    }
  },
  {
    $addFields: {
      avgRating: { $avg: "$book_reviews.rating" }
    }
  },
  {
    $project: {
      title: 1,
      authorName: { $concat: ["$book_author.name.first", " ", "$book_author.name.last"] },
      avgRating: 1
    }
  }
]);



