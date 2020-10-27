#!/usr/bin/env python3

import json
import random
import sqlite3
import argparse

from datetime import datetime

VASPS = {
    "bob": {
        "legal_person": {
            "name": {
                "name_identifiers": [{
                    "legal_person_name": "Bob's Discount VASP, PLC",
                    "legal_person_name_identifier_type": 0,
                }, {
                    "legal_person_name": "Bob VASP",
                    "legal_person_name_identifier_type": 1,
                }],
            },
            "geographic_addresses": [
                {
                    "address_type": 1,
                    "building_number": "762",
                    "street_name": "Grimsby Road",
                    "town_name": "Oxford",
                    "post_code": "OX8 U89",
                    "country": "GB",
                }
            ],
            "customer_number": "",
            "national_identification": {
                "national_identifier": "213800AQUAUP6I215N33",
                "national_identifier_type": 8,
                "country_of_issue": "GB",
                "registration_authority": "RA000589",
            },
            "country_of_registration": "GB",
        }
    },
    "alice": {
        "legal_person": {
            "name": {
                "name_identifiers": [{
                    "legal_person_name": "AliceCoin, Inc.",
                    "legal_person_name_identifier_type": 0,
                }, {
                    "legal_person_name": "Alice VASP",
                    "legal_person_name_identifier_type": 1,
                }, {
                    "legal_person_name": "AliceCoin",
                    "legal_person_name_identifier_type": 2,
                }],
            },
            "geographic_addresses": [
                {
                    "address_type": 1,
                    "building_number": "23",
                    "street_name": "Roosevelt Place",
                    "town_name": "Boston",
                    "country_sub_division": "MA",
                    "post_code": "02151",
                    "country": "US",
                }
            ],
            "customer_number": "",
            "national_identification": {
                "national_identifier": "5493004YBI24IF4TIP92",
                "national_identifier_type": 8,
                "country_of_issue": "US",
                "registration_authority": "RA000744",
            },
            "country_of_registration": "US",
        }
    },
    "evil": {
        "legal_person": {
            "name": {
                "name_identifiers": [{
                    "legal_person_name": "Evil Money Laundering GmbH",
                    "legal_person_name_identifier_type": 0,
                }, {
                    "legal_person_name": "Evil VASP",
                    "legal_person_name_identifier_type": 1,
                }],
            },
            "geographic_addresses": [
                {
                    "address_type": 1,
                    "street_name": "Rue de la Prevoté",
                    "town_name": "Guernsey",
                    "post_code": "GY8 0DS",
                    "country": "GG",
                }
            ],
            "customer_number": "",
            "national_identification": {
                "national_identifier": "549300EVILIK9WID7666",
                "national_identifier_type": 8,
                "country_of_issue": "GG",
                "registration_authority": "RA000666",
            },
            "country_of_registration": "GG",
        }
    },
}


WALLETS = [
    [
        "18nxAxBktHZDrMoJ3N2fk9imLX8xNnYbNh",
        "robert@bobvasp.co.uk", 1,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Howard",
                        "secondary_identifier": "Robert",
                        "name_identifier_type": 1,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Old Bank View",
                    "building_number": "66",
                    "post_code": "DD10 9RZ",
                    "town": "Ferryden",
                    "country": "United Kingdom",
                }],
                "national_identification": {
                    "national_identifier": "629469224",
                    "national_identifier_type": 1,
                    "country_of_issue": "GB",
                    "registration_authority": "RA000591",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1987-04-21",
                    "place_of_birth": "Oldham, United Kingdom",
                },
                "country_of_residence": "GB"
            },
        },
    ],
    [
        "1LgtLYkpaXhHDu1Ngh7x9fcBs5KuThbSzw",
        "george@bobvasp.co.uk", 1,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Kelley",
                        "secondary_identifier": "George",
                        "name_identifier_type": 1,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Colviles Park",
                    "building_number": "6",
                    "post_code": "G75 0GZ",
                    "town": "Glasgow",
                    "country": "United Kingdom",
                }],
                "national_identification": {
                    "national_identifier": "281036797",
                    "national_identifier_type": 1,
                    "country_of_issue": "GB",
                    "registration_authority": "RA000591",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1994-05-03",
                    "place_of_birth": "Guildford, United Kingdom",
                },
                "country_of_residence": "GB"
            },
        },
    ],
    [
        "14WU745djqecaJ1gmtWQGeMCFim1W5MNp3",
        "larry@bobvasp.co.uk", 1,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Clark",
                        "secondary_identifier": "Lawrence",
                        "name_identifier_type": 3,
                    }, {
                        "primary_identifier": "Clark",
                        "secondary_identifier": "Larry",
                        "name_identifier_type": 0,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Watling St",
                    "building_number": "249",
                    "post_code": "WD7 7AL",
                    "town": "Radlett",
                    "country": "United Kingdom",
                }],
                "national_identification": {
                    "national_identifier": "319560446",
                    "national_identifier_type": 5,
                    "country_of_issue": "GB",
                    "registration_authority": "RA000591",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1986-12-13",
                    "place_of_birth": "Leeds, United Kingdom",
                },
                "country_of_residence": "GB"
            },
        },
    ],
    [
       "1ASkqdo1hvydosVRvRv2j6eNnWpWLHucMX",
       "mary@alicevasp.us", 2,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "James",
                        "secondary_identifier": "Mary",
                        "name_identifier_type": 2,
                    }, {
                        "primary_identifier": "Reid",
                        "secondary_identifier": "Mary",
                        "name_identifier_type": 3,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Washington Ave",
                    "building_number": "479",
                    "post_code": "83204",
                    "town": "Pocatello",
                    "country_sub_division": "ID",
                    "country": "US",
                }],
                "national_identification": {
                    "national_identifier": "TV141121H",
                    "national_identifier_type": 3,
                    "country_of_issue": "US",
                    "registration_authority": "RA000607",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1966-08-14",
                    "place_of_birth": "Pittsfield, MA",
                },
                "country_of_residence": "US"
            },
        },
    ],
    [
        "1MRCxvEpBoY8qajrmNTSrcfXSZ2wsrGeha",
        "alice@alicevasp.us", 2,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Sanders",
                        "secondary_identifier": "Alice",
                        "name_identifier_type": 3,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Thorne Road",
                    "building_number": "78",
                    "post_code": "11801",
                    "town": "Hicksville",
                    "country_sub_division": "NY",
                    "country": "US",
                }],
                "national_identification": {
                    "national_identifier": "864 118 996",
                    "national_identifier_type": 3,
                    "country_of_issue": "US",
                    "registration_authority": "RA000628",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1975-02-18",
                    "place_of_birth": "Defiance, OH",
                },
                "country_of_residence": "US"
            },
        },
    ],
    [
        "14HmBSwec8XrcWge9Zi1ZngNia64u3Wd2v",
        "jane@alicevasp.us", 2,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Price",
                        "secondary_identifier": "Jane",
                        "name_identifier_type": 3,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Greystone Street",
                    "building_number": "28",
                    "post_code": "38017",
                    "town": "Collierville",
                    "country_sub_division": "TN",
                    "country": "US",
                }],
                "national_identification": {
                    "national_identifier": "112502920",
                    "national_identifier_type": 6,
                    "country_of_issue": "US",
                    "registration_authority": "RA000748",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1992-10-04",
                    "place_of_birth": "West Islip, NY",
                },
                "country_of_residence": "US"
            },
        },
    ],
    [
        "1PFTsUQrRqvmFkJunfuQbSC2k9p4RfxYLF",
        "voldemort@evilvasp.gg", 3,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Riddle",
                        "secondary_identifier": "Tom Marvolo",
                        "name_identifier_type": 3,
                    }, {
                        "primary_identifier": "Voldemort",
                        "secondary_identifier": "",
                        "name_identifier_type": 0,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Ballagawne Road",
                    "building_number": "97",
                    "town": "Rushen",
                    "country": "Isle of Man",
                }],
                "national_identification": {
                    "national_identifier": "304402330",
                    "national_identifier_type": 1,
                    "country_of_issue": "IM",
                    "registration_authority": "RA000405",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1926-12-31",
                    "place_of_birth": "London, United Kingdom",
                },
                "country_of_residence": "IM"
            },
        },
    ],
    [
        "172n89jLjXKmFJni1vwV5EzxKRXuAAoxUz",
        "adolf@evilvasp.gg", 3,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Sokoloa",
                        "secondary_identifier": "Radomil",
                        "name_identifier_type": 4,
                    }, {
                        "primary_identifier": "Hitler",
                        "secondary_identifier": "Adolph",
                        "name_identifier_type": 1,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Комарова Ул., дом 7, кв.",
                    "building_number": "100",
                    "town": "Красноярск",
                    "country_sub_division": "Красноярский край",
                    "country": "RU",
                }],
                "national_identification": {
                    "national_identifier": "529452906",
                    "national_identifier_type": 1,
                    "country_of_issue": "RU",
                    "registration_authority": "RA000499",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1989-04-20",
                    "place_of_birth": "Braunau am Inn, Austria",
                },
                "country_of_residence": "RU"
            },
        },
    ],
    [
        "182kF4mb5SW4KGEvBSbyXTpDWy8rK1Dpu",
        "mildred@evilvasp.gg", 3,
        {
            "natural_person": {
                "name": {
                    "name_identifiers": [{
                        "primary_identifier": "Ratched",
                        "secondary_identifier": "Mildred",
                        "name_identifier_type": 1,
                    }],
                },
                "geographic_addresses": [{
                    "address_type": 0,
                    "street_name": "Overlook Road",
                    "building_number": "6222",
                    "post_code": "36618",
                    "town": "Mobile",
                    "country_sub_division": "AL",
                    "country": "United States",
                }],
                "national_identification": {
                    "national_identifier": "201490313",
                    "national_identifier_type": 1,
                    "country_of_issue": "US",
                    "registration_authority": "RA000595",
                },
                "customer_identification": "",
                "date_and_place_of_birth": {
                    "date_of_birth": "1975-09-21",
                    "place_of_birth": "Salem, Oregon",
                },
                "country_of_residence": "US"
            },
        },
    ],
]


def clean(conn):
    cur = conn.cursor()
    for table in ["transactions", "accounts", "wallets", "vasps"]:
        cur.execute(f"DELETE FROM {table}")
    cur.close()
    conn.commit()


def create_vasps(conn, vasp):
    params = []
    sql = "INSERT INTO vasps (id, name, is_local, ivms101, created_at, updated_at) VALUES (?,?,?,?,?,?)"
    cur = conn.cursor()

    for i, (name, record) in enumerate(VASPS.items()):
        # TODO: look up VASP ID in Directory Service
        ts = datetime.now()
        is_local = name == vasp
        name = record["legal_person"]["name"]["name_identifiers"][0]["legal_person_name"]

        # Only store IVMS data if this is the local VASP
        # (so that VASPs have to look each other up in the directory service)
        record = json.dumps(record) if is_local else None
        params.append([i+1, name, is_local, record, ts, ts])

    cur.executemany(sql, params)


def create_wallets(conn, vasp):
    params = []
    cur = conn.cursor()
    sql = "INSERT INTO wallets (address, email, provider_id, created_at, updated_at) VALUES (?,?,?,?,?)"

    for wallet in WALLETS:
        ts = datetime.now()
        params.append([wallet[0], wallet[1], wallet[2], ts, ts])

    cur.executemany(sql, params)


def create_accounts(conn, vasp):
    params = []
    cur = conn.cursor()
    sql = "INSERT INTO accounts (name, email, wallet_address, ivms101, created_at, updated_at) VALUES (?,?,?,?,?,?)"

    for wallet in WALLETS:
        domain = wallet[1].split("@")[-1]
        if not domain.startswith(vasp):
            continue

        # If the wallet belongs to the VASP assign it a "customer identification"
        wallet[3]["natural_person"]["customer_identification"] = random.randint(100, 10000)

        # Get the name of the person for the account
        name_parts = wallet[3]["natural_person"]["name"]["name_identifiers"][0]
        name = "{secondary_identifier} {primary_identifier}".format(**name_parts)
        ivms = json.dumps(wallet[3])
        ts = datetime.now()

        params.append([name, wallet[1], wallet[0], ivms, ts, ts])

    cur.executemany(sql, params)


def main(args):
    with sqlite3.connect(args.db) as conn:
        if args.clean:
            clean(conn)

        create_vasps(conn, args.vasp)
        create_wallets(conn, args.vasp)
        create_accounts(conn, args.vasp)
        conn.commit()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="generates database fixtures for an rVASP"
    )
    parser.add_argument(
        "-v", "--vasp", choices={"bob", "alice", "evil"}, required=True,
        help="name of the VASP to generate the database for",
    )
    parser.add_argument(
        "-c", "--clean", action="store_true",
        help="clean up anything in the tables before populating",
    )
    parser.add_argument(
        "-d", "--db", default="rvasp.db",
        help="path to sqlite3 database to connect to",
    )

    args = parser.parse_args()
    main(args)