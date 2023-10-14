import asyncio

from keras.src.utils import to_categorical
from tqdm import tqdm

from database.async_db import DataBase
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from database.Db_objects import Branch
import numpy as np


class Vectorized:
    rko: list[int]
    officeType: list[int]
    salePointFormat: list[int]
    suoAvailability: list[int]
    hasRamps: list[int]
    keps: list[int]
    myBranchs: list[int]
    functions: list[int]


def to_np(s: set) -> np.array:
    return np.array(list([s]))


class BigEncoder:
    rkos: set[str] = set()
    rko_e: LabelEncoder = LabelEncoder()
    officeTypes: set[str] = set()
    officeType_e: LabelEncoder = LabelEncoder()
    salePointFormats: set[str] = set()
    salePointFormat_e: LabelEncoder = LabelEncoder()
    suoAvailabilitys: set[str] = set()
    suoAvailability_e: LabelEncoder = LabelEncoder()
    hasRamps: set[str] = set()
    hasRamp_e: LabelEncoder = LabelEncoder()
    keps: set[bool] = set()
    kep_e: LabelEncoder = LabelEncoder()
    myBranchs: set[bool] = set()
    myBranch_e: LabelEncoder = LabelEncoder()
    functions: set[str] = set()
    function_e: LabelEncoder = LabelEncoder()

    def fit(self):
        self.rko_e.fit(to_np(self.rkos))
        self.officeType_e.fit(to_np(self.officeTypes))
        self.salePointFormat_e.fit(to_np(self.salePointFormats))
        self.suoAvailability_e.fit(to_np(self.suoAvailabilitys))
        self.hasRamp_e.fit(to_np(self.hasRamps))
        self.kep_e.fit(to_np(self.keps))
        self.myBranch_e.fit(to_np(self.myBranchs))
        self.function_e.fit(to_np(self.functions))

    def transform(self, b: Branch) -> Vectorized:
        v = Vectorized()
        v.rko = to_categorical(self.rko_e.transform(to_np(b.rko)))
        v.officeType = to_categorical(self.officeType_e.transform(to_np(b.officetype)))
        v.salePointFormat = to_categorical(self.salePointFormat_e.transform(to_np(b.salepointformat)))
        v.suoAvailability = to_categorical(self.suoAvailability_e.transform(to_np(b.suoavailability)))
        v.hasRamps = to_categorical(self.hasRamp_e.transform(to_np(b.hasramp)))
        v.keps = to_categorical(self.kep_e.transform(to_np(b.kep)))
        v.myBranchs = to_categorical(self.myBranch_e.transform(to_np(b.mybranch)))
        f = set()
        for i in b.functions:
           f.add(i.function_name)
        v.functions = to_categorical(self.function_e.transform(to_np(set(f))))

        return v


async def to_vector():
    db = DataBase()
    be = BigEncoder()
    brances = await db.get_brances()
    for i in tqdm(brances):
        be.rkos.add(i.rko)
        be.officeTypes.add(i.officetype)
        be.salePointFormats.add(i.salepointformat)
        be.hasRamps.add(i.hasramp)
        be.keps.add(i.kep)
        be.myBranchs.add(i.mybranch)
        for f in i.functions:
            be.functions.add(f.function_name)

    be.fit()
    t = be.transform(brances[0])
    pass


if __name__ == '__main__':
    asyncio.run(to_vector())
