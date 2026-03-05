# 구현 상세 계획서: 지면 인지형 고효율 혼합 재배 시스템

## 1. 접근 방식 및 아키텍처
제공된 함수 명세를 기반으로, 높은 틱 비용을 가진 `till()`과 `spawn_drone()`의 호출을 최소화하면서 지면 적합성을 100% 보장하는 아키텍처를 설계합니다.

- [x] `functions.py`: `for_all` 함수에서 `num_drones()`를 체크하여 `spawn_drone()` 호출 전 비용 절감 로직 추가 (완료)
- [x] `Mega_Crops.py`: `mixed_worker_logic`에서 `till()` 호출 전 `get_ground_type()` 비교 연산 필수 적용 (완료)
- [x] `Mega_Crops.py`: 틱 비용이 높은 `till()`을 줄이기 위해 가능한 한 지면 변경을 최소화하는 식재 순서 고려 (완료)
- [x] `Mega_Crops.py`: `mixed_worker_logic` 내 튜플 인덱싱 및 `== None` 문법 안정성 재검토 (완료)

## 2. 수정 대상 파일 및 경로
- `functions.py`: 공통 병렬 유틸리티 및 동기화 로직
- `Mega_Crops.py`: 고효율 혼합 재배 워커 및 메인 오케스트레이터

## 3. 코드 스니펫 (Code Snippets)

### 비용 최적화된 for_all (`functions.py`)
```python
def for_all(f):
    drones = []
    def row_task():
        for _ in range(WORLD_SIZE - 1):
            f()
            move(East)
        f()
    
    for _ in range(WORLD_SIZE):
        # 1틱 비용의 num_drones()로 200틱 비용의 spawn_drone() 호출을 방어
        if num_drones() < max_drones():
            d = spawn_drone(row_task)
            if d == None:
                row_task()
            else:
                drones.append(d)
        else:
            row_task()
        move(North)
    
    for i in range(len(drones)):
        wait_for(drones[i])
    go_zero()
```

### 지면 상태 확인 및 토글 방지 로직 (`Mega_Crops.py`)
```python
def mixed_worker_logic(start_x):
    for start_y in range(WORLD_SIZE):
        go(start_x, start_y)
        
        if get_entity_type() == None:
            # 1. 초기 지면 설정 (Grassland 보장)
            if get_ground_type() == Grounds.Soil:
                till() # Soil -> Grassland (200틱 소모)
            plant(Entities.Grass)
            
            for i in range(5):
                companion = get_companion()
                if companion == None: break
                
                target_type = companion[0]
                pos = companion[1]
                go(pos[0], pos[1])
                
                if get_entity_type() == None:
                    # 2. 타겟 지면 최적화
                    current_ground = get_ground_type()
                    
                    if target_type == Entities.Grass:
                        # Grass는 Grassland가 필요함
                        if current_ground == Grounds.Soil:
                            till() # 200틱 소모
                    else:
                        # 그 외 작물은 Soil이 필요함
                        if current_ground == Grounds.Grassland:
                            till() # 200틱 소모
                    
                    plant(target_type)
                else:
                    break
```

## 4. 고려 사항 및 트레이드오프
- **지면 전환 비용 (200틱)**: `till()`이 매우 무겁기 때문에, 한 번 `Soil`로 바꾼 구역은 가급적 `Soil` 요구 작물을 우선 배치하는 것이 좋으나 `Mixed Cultivation`의 무작위성 때문에 완전한 배제는 어렵습니다.
- **안정성 vs 속도**: `can_move()`를 사용하여 미로 등 장애물 상황에서도 드론이 멈추지 않도록 네비게이션을 보강할 수 있습니다.
- **동기화 정확도**: `wait_for` 사용 시 반환값을 체크하여 드론의 작업 성공 여부를 판단할 수 있으나, 현재 시스템에서는 종료 대기 자체에 집중합니다.
