# 시스템 리서치 보고서: 지면(Ground) 및 개체(Entity) 메커니즘 분석

## 1. 시스템 구조 및 동작 원리
본 시스템은 지면 타입(`Grounds`)과 그 위에 심어지는 개체 타입(`Entities`)을 엄격히 구분합니다.
- **Grassland**: 기본 지면 상태. `Entities.Grass`는 이 지면에서만 자라며, 수확 후에도 `Grassland` 상태가 유지됩니다.
- **Soil**: `till()` 함수를 통해 `Grassland`를 변형시킨 상태. `Carrot`, `Bush`, `Tree`, `Pumpkin` 등 대부분의 작물은 이 지면에서만 파종 가능합니다.
- **혼합 재배 시너지**: `get_companion()`은 지면과 상관없이 현재 위치의 개체가 원하는 다음 동반 식물과 좌표를 반환합니다.

## 2. 주요 함수 및 레이어 관계
- **`get_ground_type()`**: 현재 타일의 지면이 `Grounds.Grassland`인지 `Grounds.Soil`인지 반환합니다.
- **`till()`**: 지면 타입을 전환합니다 (`Grassland` <-> `Soil`).
- **`plant(entity)`**: 지면 타입이 해당 개체의 요구 조건과 맞지 않으면 실행되지 않거나 실패합니다.
  - `Entities.Grass`: `Grassland` 필요.
  - `Entities.Bush`, `Entities.Tree`, `Entities.Carrot`: `Soil` 필요.

## 3. 잠재적 위험 요소 (사이드 이펙트) 및 오류 원인 분석
- **지면 부적합으로 인한 파종 실패**: 기존 로직은 `Entities.Carrot`일 때만 `till()`을 수행했습니다. 하지만 `Bush`나 `Tree`를 심을 때 지면이 `Grassland`라면 파종에 실패하고 드론은 아무것도 심지 못한 채 다음 좌표로 이동(방황)하게 됩니다.
- **동기화 오류**: `for_all`이 완료되기 전 파종이 시작되어, 지면이 제대로 준비되지 않은 상태에서 로직이 꼬이는 현상이 발생합니다.

## 4. 해결 방안
1. **지면 타입 체크 자동화**: `mixed_worker_logic`에서 심으려는 작물에 따라 `get_ground_type()`을 체크하고 필요한 경우 `till()`을 호출합니다.
2. **초기화 동기화 보장**: `for_all` 내부에 `wait_for`를 확실히 구현하여 모든 타일의 지면 준비를 마친 후 파종을 시작합니다.
